from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Propriedade, Reserva, Pagamento
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404

import re

# Formulário que permite o cadastro de um usuário no sistema
# Possui validadores internos, fornecidos pela classe UserCreationForm
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

# Formulário que permite a atualização dos dados de um usuário no sistema
# Possui validadores internos, fornecidos pelo model User
class AtualizarUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

# Formulário que permite o cadastro de uma propriedade no sistema
# Possui validadores para o campo CEP
# E possui campos escondidos que são setados pelo sistema
class PropriedadeForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = '__all__'

        widgets = {
            'id': forms.HiddenInput(attrs={}),
            'proprietario': forms.HiddenInput(attrs={}),
            'imagem': forms.ClearableFileInput(),
        }
    
    def clean_CEP(self):
        CEP = self.cleaned_data['CEP']
        if not re.match('^\d{5}-\d{3}', CEP):
            self.add_error('CEP', 'CEP inválido')
        return CEP

# Formulário que permite a atualização dos dados de uma 
# Propriedade no sistema
class PropriedadeEditForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = ['nome', 'descricao', 'imagem']

# Formulário que permite a atualização dos dados de uma 
# Reserva no sistema
class ReservaEditForm(forms.ModelForm):
    class Meta:
        model = Reserva

        fields = ['qtd_pessoas']

# Formulário que permite o cadastro de uma reserva no sistema
# Possui validadores para os campos dini (data inicial),
# dfim (data final), a fim de evitar que reservas sejam feitas
# No passado ou que reservas sejam feitas em datas que a propriedade
# Já esteja reservada
# E possui campos escondidos que são setados pelo sistema
class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva

        fields = '__all__'

        widgets = {
            'id': forms.HiddenInput(attrs={'readonly':'True'}),
            'hospede': forms.HiddenInput(attrs={'readonly':'True'}),
            'propriedade': forms.HiddenInput(attrs={'readonly':'True'}),
            'dados_pagamento': forms.HiddenInput(attrs={'readonly':'True'}),
            'dini': forms.DateInput(attrs={'type': 'date'}),
            'dfim': forms.DateInput(attrs={'type': 'date'}),
            'qtd_pessoas': forms.Select()
        }
    def __init__(self, *args, **kwargs):
        super(ReservaForm, self).__init__(*args, **kwargs)
        self.fields['qtd_pessoas'].label = 'Pessoas'

    def clean(self):
        cleaned_data = super().clean()
        dini = cleaned_data['dini']
        dfim = cleaned_data['dfim']
        propriedade = cleaned_data['propriedade']

        deletou_ini = False
        deletou_fim = False

        if dini < datetime.date.today():
            self._errors['dini'] = self.error_class(['A data não pode ser no passado'])
            deletou_ini = True

        if dfim < datetime.date.today() or dfim < dini:
            if dfim < dini:
                self._errors['dfim'] = self.error_class(['A data final não pode ser maior que a inicial'])
            else:
                self._errors['dfim'] = self.error_class(['A data não pode ser no passado'])
            deletou_fim = True
        if (not deletou_ini and not deletou_fim):
            reservas = Reserva.objects.filter(propriedade = propriedade).filter(
                Q(dini__lte=dini, dfim__gte=dfim)
            )
            if reservas:
                self._errors['dini'] = self.error_class(['Já existe uma reserva com essas datas'])
                self._errors['dfim'] = self.error_class(['Já existe uma reserva com essas datas'])
                deletou_ini = True
                deletou_fim = True

        if deletou_ini:
            del self.cleaned_data['dini']
        if deletou_fim:
            del self.cleaned_data['dfim']

        return cleaned_data

# Formulário que permite a atualização dos dados de um 
# Pagamento no sistema
class PagamentoEditForm(forms.ModelForm):
    class Meta:
        model = Pagamento

        fields = ['tipo_pagamento']

    def __init__(self, *args, **kwargs):
        super(PagamentoEditForm, self).__init__(*args, **kwargs)
        self.fields['tipo_pagamento'].label = 'Tipo de pagamento'

# Formulário que permite o cadastro de um pagamento no sistema
# É exibido junto com o formulário ReservaForm
# Possui campos escondidos que são setados pelo sistema
class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento

        fields = '__all__'

        widgets = {
            'status': forms.HiddenInput(attrs={'readonly':'True'}),
            'id_transacao': forms.HiddenInput(attrs={'readonly':'True'})
        }

    def __init__(self, *args, **kwargs):
        super(PagamentoForm, self).__init__(*args, **kwargs)
        self.fields['tipo_pagamento'].label = 'Tipo de pagamento'

# Formulário que permite que uma propriedade seja buscada no sistema
# Para que uma reserva seja efetuada
# Possui validadores nos campos de data_ini e data_fim
# A fim de evitar que não seja possível pesquisar datas no passado
class BuscaPropForm(forms.Form):
    cidade = forms.CharField(label='Cidade', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_ini = forms.DateField(label='Data de entrada', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    data_fim = forms.DateField(label='Data de saída', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def clean_data_ini(self):
        data_ini = self.cleaned_data['data_ini']
        if data_ini < datetime.date.today():
            self.add_error('data_ini', 'A data não pode ser no passado')
        return data_ini
    
    def clean_data_fim(self):
        cleaned_data = super().clean()
        data_ini = cleaned_data['data_ini']
        data_fim = cleaned_data['data_fim']
        if data_fim < datetime.date.today():
            self.add_error('data_fim', 'A data não pode ser no passado')
        if data_fim < data_ini:
            self.add_error('data_fim', 'Data inválida')
        return data_fim

