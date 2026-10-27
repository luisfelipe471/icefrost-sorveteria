from io import BytesIO
from tempfile import TemporaryDirectory

from PIL import Image
from django.contrib.auth import get_user_model
from django.core.validators import MaxLengthValidator
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .forms import CadastroUsuarioForm
from .models import Categoria, Feedback, Fornecedor, OpcaoDietetica, Sorvete


class PublicPagesTests(TestCase):
	def test_public_pages_are_available_to_visitors(self):
		for page in ('index', 'cardapio', 'galeria', 'login', 'cadastrar_usuario'):
			with self.subTest(page=page):
				response = self.client.get(reverse(page))
				self.assertEqual(response.status_code, 200)

	def test_main_navigation_is_visible_to_visitors(self):
		response = self.client.get(reverse('index'))

		for page in ('cardapio', 'galeria'):
			with self.subTest(page=page):
				self.assertContains(response, f'href="{reverse(page)}"')

		self.assertNotContains(response, f'href="{reverse("feedback")}"')
		self.assertNotContains(response, 'Cadastrar Sorvete')

	def test_login_form_is_inside_white_panel(self):
		response = self.client.get(reverse('login'))

		self.assertContains(response, 'class="form-panel login-panel"')
		self.assertContains(response, 'Acesso Restrito')

	def test_username_is_limited_to_30_characters(self):
		form = CadastroUsuarioForm({
			'username': 'x' * 31,
			'password1': 'SafePass!234',
			'password2': 'SafePass!234',
		})
		username_field = form.fields['username']

		self.assertEqual(username_field.max_length, 30)
		self.assertEqual(username_field.widget.attrs['maxlength'], 30)
		self.assertIn('Até 30 caracteres.', username_field.help_text)
		self.assertTrue(any(
			isinstance(validator, MaxLengthValidator) and validator.limit_value == 30
			for validator in username_field.validators
		))
		self.assertFalse(form.is_valid())
		self.assertIn('Use no máximo 30 caracteres.', form.errors['username'])

	def test_common_password_rule_is_not_shown_or_enforced(self):
		form = CadastroUsuarioForm({
			'username': 'icefrost-user',
			'password1': 'password',
			'password2': 'password',
		})

		self.assertNotIn('comumente utilizada', str(form.fields['password1'].help_text))
		self.assertTrue(form.is_valid(), form.errors)

	def test_feedback_requires_authentication(self):
		response = self.client.get(reverse('feedback'))

		self.assertEqual(response.status_code, 302)

	def test_authenticated_user_can_access_feedback(self):
		user = get_user_model().objects.create_user(username='cliente', password='SenhaForte123!')
		self.client.force_login(user)

		response = self.client.get(reverse('feedback'))

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, f'href="{reverse("feedback")}"')

	def test_gallery_has_all_images_and_accessible_modal(self):
		response = self.client.get(reverse('galeria'))

		self.assertContains(response, 'img/10.jpg')
		self.assertContains(response, 'aria-modal="true"')
		self.assertContains(response, 'Fechar imagem')

	def test_feedback_submission_displays_name_and_message(self):
		user = get_user_model().objects.create_user(username='cliente-feedback', password='SenhaForte123!')
		self.client.force_login(user)

		first_response = self.client.post(reverse('feedback'), {
			'nome': 'Ana Souza',
			'email': 'ana@example.com',
			'mensagem': 'Adorei a sorveteria!',
		})
		second_response = self.client.post(reverse('feedback'), {
			'nome': 'Rafa',
			'email': 'rafa@example.com',
			'mensagem': 'Quero voltar em breve.',
		})
		response = self.client.get(reverse('feedback'))

		self.assertRedirects(first_response, reverse('feedback'))
		self.assertRedirects(second_response, reverse('feedback'))
		self.assertEqual(Feedback.objects.count(), 2)
		self.assertContains(response, 'Ana Souza')
		self.assertContains(response, 'Adorei a sorveteria!')
		self.assertContains(response, 'Rafa')
		self.assertContains(response, 'Quero voltar em breve.')
		self.assertContains(response, 'class="feedback-list"')
		response_html = response.content.decode()
		self.assertLess(response_html.index('</section>'), response_html.index('class="feedback-list"'))
		self.assertLess(response_html.index('Rafa'), response_html.index('Ana Souza'))


class SorveteAccessTests(TestCase):
	def test_catalog_management_requires_authentication(self):
		response = self.client.get(reverse('cadastrar_sorvete'))

		self.assertEqual(response.status_code, 302)

	def test_customers_cannot_see_or_access_catalog_management(self):
		user = get_user_model().objects.create_user(username='visitante', password='SenhaForte123!')
		self.client.force_login(user)

		response = self.client.get(reverse('index'))

		self.assertNotContains(response, 'Cadastrar Sorvete')
		self.assertEqual(self.client.get(reverse('cadastrar_sorvete')).status_code, 302)

	def test_staff_users_see_and_can_access_catalog_management(self):
		user = get_user_model().objects.create_user(
			username='equipe', password='SenhaForte123!', is_staff=True
		)
		self.client.force_login(user)

		response = self.client.get(reverse('index'))

		self.assertContains(response, 'Cadastrar Sorvete')
		self.assertEqual(self.client.get(reverse('cadastrar_sorvete')).status_code, 200)


class CardapioTests(TestCase):
	def setUp(self):
		self.massa = Categoria.objects.create(nome='Massa')
		self.picole = Categoria.objects.create(nome='Picolé')
		self.fornecedor = Fornecedor.objects.create(
			nome_empresa='Fornecedor de teste',
			telefone='11999999999',
			email='fornecedor@example.com',
		)
		self.sem_gluten = OpcaoDietetica.objects.create(nome='Sem Glúten')
		self.vegano = OpcaoDietetica.objects.create(nome='Vegano')
		self.chocolate = Sorvete.objects.create(
			sabor='Chocolate Belga',
			descricao='Sorvete cremoso de cacau.',
			preco='25.00',
			categoria=self.massa,
			fornecedor=self.fornecedor,
		)
		self.chocolate.opcoes_dieteticas.add(self.sem_gluten)
		self.morango = Sorvete.objects.create(
			sabor='Morango Diet',
			descricao='Picolé de morango natural.',
			preco='5.00',
			categoria=self.picole,
			fornecedor=self.fornecedor,
		)
		self.morango.opcoes_dieteticas.add(self.vegano)

	def test_menu_has_one_white_container(self):
		response = self.client.get(reverse('cardapio'))

		self.assertContains(response, 'class="catalog-container"')

	def test_known_flavors_use_matching_default_photos(self):
		response = self.client.get(reverse('cardapio'))

		self.assertContains(response, 'src="/static/img/menu-chocolate.jpg"')
		self.assertContains(response, 'alt="Sorvete de Chocolate Belga"')
		self.assertContains(response, 'src="/static/img/menu-morango.jpg"')
		self.assertContains(response, 'alt="Sorvete de Morango Diet"')

	def test_search_filters_flavors_by_name_or_description(self):
		response = self.client.get(reverse('cardapio'), {'q': 'cacau'})

		self.assertContains(response, 'Chocolate Belga')
		self.assertNotContains(response, 'Morango Diet')

	def test_category_and_dietary_filters(self):
		category_response = self.client.get(reverse('cardapio'), {'categoria': self.picole.id})
		dietary_response = self.client.get(reverse('cardapio'), {'opcao_dietetica': self.vegano.id})

		self.assertContains(category_response, 'Morango Diet')
		self.assertNotContains(category_response, 'Chocolate Belga')
		self.assertContains(dietary_response, 'Morango Diet')
		self.assertNotContains(dietary_response, 'Chocolate Belga')

	def test_staff_can_upload_and_display_flavor_photo(self):
		staff_user = get_user_model().objects.create_user(
			username='equipe-fotos', password='SenhaForte123!', is_staff=True
		)
		self.client.force_login(staff_user)
		image_buffer = BytesIO()
		Image.new('RGB', (90, 60), color='pink').save(image_buffer, format='JPEG')
		image_buffer.seek(0)
		image_upload = SimpleUploadedFile('morango.jpg', image_buffer.read(), content_type='image/jpeg')

		with TemporaryDirectory() as media_root, override_settings(MEDIA_ROOT=media_root):
			response = self.client.post(reverse('cadastrar_sorvete'), {
				'sabor': 'Morango com foto',
				'descricao': 'Sorvete de morango.',
				'imagem': image_upload,
				'preco': '12.50',
				'categoria': self.massa.id,
				'fornecedor': self.fornecedor.id,
				'opcoes_dieteticas': [self.sem_gluten.id],
			})

			self.assertEqual(response.status_code, 302)
			self.assertEqual(self.client.get(reverse('cardapio')).status_code, 200)
			self.assertContains(
				self.client.get(reverse('cardapio')),
				'src="/media/sorvetes/morango.jpg"',
			)
