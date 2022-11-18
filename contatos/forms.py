from django import forms
from .models import Contato, Categoria

class ContatoForm(forms.ModelForm):
    class Meta:
        model = Contato
        fields = ['nome', 'sobrenome', 'telefone', 'email', 'descricao', 'categoria', 'foto']
        
class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome']