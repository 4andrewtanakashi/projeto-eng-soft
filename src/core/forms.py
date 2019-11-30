from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Propriedade, Reserva, Pagamento
from django.contrib.auth.models import User


class PropriedadeForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = '__all__'

        widgets = {
            'id': forms.HiddenInput(),
            'proprietario': forms.HiddenInput(),
            'status': forms.HiddenInput(),
        }
'''
class RegistrarForm(UserCreationForm):
    usuario = forms.CharField(label="Usuario")
    senha1 = forms.CharField(label="Digite sua senha", widget=forms.PasswordInput)
    senha2 = forms.CharField(label="Digite sua senha novamente", widget=forms.PasswordInput)
    email = forms.EmailField(label="E-mail")
    nome = forms.CharField(label="Nome")

    class Meta:
        model = User
        fields = ("username", "senha1", "senha2", "email", "nome")

    def save(self, commit=True):
        user = super(RegistrarForm, self).save(commit=False)
        prim_nome, seg_nome = self.cleaned_data["fullname"].split()
        user.username = self.cleaned_data["usuario"]
        user.password1 = self.cleaned_data["senha1"]
        user.password2 = self.cleaned_data["senha2"]
        user.first_name = prim_nome
        user.last_name = seg_nome
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
'''

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva

        fields = '__all__'

        widgets = {
            'hospede': forms.HiddenInput(),
            'propriedade': forms.HiddenInput(),
            'dados_pagamento': forms.HiddenInput(),
            'ini': forms.DateInput(attrs={'type': 'date'}),
            'fim': forms.DateInput(attrs={'type': 'date'}),
            'qtd_pessoas': forms.Select()
        }

class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento

        fields = '__all__'

        widgets = {
            'tipo_pagamento': forms.RadioSelect(choices=Pagamento.ESCOLHAS_PAGAMENTO),
            'status': forms.HiddenInput(),
            'id_transacao': forms.HiddenInput()
        }

class BuscaPropForm(forms.Form):
    cidade = forms.CharField(label='cidade', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_ini = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    data_fim = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))


