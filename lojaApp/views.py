from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.templatetags.static import static
from .models import Categoria, Comentario, Feedback, OpcaoDietetica, Sorvete
from .forms import SorveteForm, ComentarioForm, FeedbackForm, CadastroUsuarioForm
from django.contrib.auth import logout as auth_logout

DEFAULT_CARD_IMAGES = {
    'Baunilha Zero': 'img/menu-baunilha.jpg',
    'Chocolate Belga': 'img/menu-chocolate.jpg',
    'Coco Branco': 'img/menu-coco.jpg',
    'Limão Siciliano': 'img/menu-limao.jpg',
    'Maracujá (Sorbet)': 'img/menu-maracuja.jpg',
    'Milk Shake Oreo': 'img/menu-oreo.jpg',
    'Morango Diet': 'img/menu-morango.jpg',
    'Ninho com Nutella': 'img/menu-ninho-nutella.jpg',
    'Pistache Premium': 'img/menu-pistache.jpg',
    'Shake Paçoca': 'img/menu-pacoca.jpg',
}



def index(request):
    return render(request, 'lojaApp/index.html')

def mostrar_cardapio(request):
    sorvetes = Sorvete.objects.select_related('categoria').prefetch_related('opcoes_dieteticas')
    busca = request.GET.get('q', '').strip()
    categoria = request.GET.get('categoria', '')
    opcao_dietetica = request.GET.get('opcao_dietetica', '')

    if busca:
        sorvetes = sorvetes.filter(Q(sabor__icontains=busca) | Q(descricao__icontains=busca))
    if categoria.isdigit():
        sorvetes = sorvetes.filter(categoria_id=categoria)
    if opcao_dietetica.isdigit():
        sorvetes = sorvetes.filter(opcoes_dieteticas__id=opcao_dietetica)

    sorvetes = list(sorvetes.distinct().order_by('sabor'))
    for sorvete in sorvetes:
        imagem_padrao = DEFAULT_CARD_IMAGES.get(sorvete.sabor)
        sorvete.card_image_url = (
            sorvete.imagem.url if sorvete.imagem else static(imagem_padrao) if imagem_padrao else ''
        )

    return render(request, 'lojaApp/cardapio.html', {
        'sorvetes': sorvetes,
        'categorias': Categoria.objects.order_by('nome'),
        'opcoes_dieteticas': OpcaoDietetica.objects.order_by('nome'),
        'busca': busca,
        'categoria_selecionada': categoria,
        'opcao_selecionada': opcao_dietetica,
        'filtros_aplicados': bool(busca or categoria or opcao_dietetica),
    })

@login_required
def comentario_sorvete(request, sorvete_id):
    sorvete = get_object_or_404(Sorvete, id=sorvete_id)
    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.autor = sorvete.sabor
            comentario.save()
            messages.success(request, 'Comentário enviado com sucesso!')
            return redirect('cardapio')
    else:
        form = ComentarioForm()
    return render(request, 'lojaApp/form_comentario.html', {'sorvete': sorvete, 'form': form})


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'lojaApp/cadastrar_usuario.html', {'form': form})


@staff_member_required
def cadastrar_sorvete(request):
    if request.method == 'POST':
        form = SorveteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('cardapio')
    else:
        form = SorveteForm()

    return render(request, 'lojaApp/form_sorvete.html', {'form': form})


@staff_member_required
def editar_sorvete(request, sorvete_id):
    sorvete = get_object_or_404(Sorvete, id=sorvete_id)
    if request.method == 'POST':
        form = SorveteForm(request.POST, request.FILES, instance=sorvete)
        if form.is_valid():
            form.save()
            return redirect('cardapio')
    else:
        form = SorveteForm(instance=sorvete)

    return render(request, 'lojaApp/form_sorvete.html', {'form': form, 'sorvete': sorvete})


@staff_member_required
def excluir_sorvete(request, sorvete_id):
    sorvete = get_object_or_404(Sorvete, id=sorvete_id)
    if request.method == 'POST':
        sorvete.delete()
        return redirect('cardapio')

    return render(request, 'lojaApp/form_exclusao.html', {'sorvete': sorvete})


@login_required
def feedback(request):
    mensagem = None
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            Feedback.objects.create(
                nome=form.cleaned_data['nome'],
                email=form.cleaned_data['email'],
                mensagem=form.cleaned_data['mensagem'],
            )
            messages.success(request, 'Seu feedback foi enviado com sucesso!')
            return redirect('feedback')

        mensagem = 'Houve um erro ao enviar seu feedback. Por favor, tente novamente.'
    else:
        form = FeedbackForm()

    return render(request, 'lojaApp/feedback.html', {
        'form': form,
        'mensagem': mensagem,
        'feedbacks': Feedback.objects.all() if request.user.is_staff else Feedback.objects.none(),
    })

def logout_view(request):
    auth_logout(request)
    return redirect('index')