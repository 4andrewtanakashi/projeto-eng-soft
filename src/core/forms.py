from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Propriedade, Reserva, Pagamento
from django.contrib.auth.models import User

class RegistrarForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Obrigatório. O seu primeiro nome.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Obrigatório. O seu último nome.')
    email = forms.EmailField(max_length=254, help_text='Obrigatório. Informe um email válido.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super(RegistrarForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Primeiro nome'
        self.fields['last_name'].label = 'Último nome'

class PropriedadeForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = '__all__'

        widgets = {
            'id': forms.HiddenInput(),
            'proprietario': forms.HiddenInput(),
            'status': forms.HiddenInput(),
        }

class PropriedadeEditForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = ['nome', 'descricao', 'imagem']


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva

        fields = '__all__'

        widgets = {
            'id': forms.HiddenInput(attrs={'readonly':'True'}),
            'hospede': forms.HiddenInput(),
            'propriedade': forms.HiddenInput(),
            'dados_pagamento': forms.HiddenInput(),
            'dini': forms.DateInput(attrs={'type': 'date'}),
            'dfim': forms.DateInput(attrs={'type': 'date'}),
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



