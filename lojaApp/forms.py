from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MaxLengthValidator

from .models import Sorvete, Comentario


class CadastroUsuarioForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        campo_usuario = self.fields['username']
        campo_usuario.max_length = 30
        campo_usuario.validators.append(
            MaxLengthValidator(30, message='Use no máximo 30 caracteres.')
        )
        campo_usuario.widget.attrs['maxlength'] = 30
        campo_usuario.help_text = 'Até 30 caracteres. Use letras, números e @/./+/-/_.'


class SorveteForm(forms.ModelForm):
    class Meta:
        model = Sorvete
        fields = ['sabor', 'descricao', 'imagem', 'preco', 'categoria', 'fornecedor', 'opcoes_dieteticas']


class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['email', 'mensagem']


class FeedbackForm(forms.Form):
    nome = forms.CharField(label='Seu nome', max_length=100)
    email = forms.EmailField(label='E-mail')
    mensagem = forms.CharField(label='Mensagem', widget=forms.Textarea)