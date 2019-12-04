from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Propriedade, Reserva, Pagamento
from django.contrib.auth.models import User
import datetime
from django.db.models import Q
from django.shortcuts import get_object_or_404

import re

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
            'id': forms.HiddenInput(attrs={'readonly':'True'}),
            'proprietario': forms.HiddenInput(attrs={'readonly':'True'}),
            'imagem': forms.ClearableFileInput(),
        }
    
    def clean_CEP(self):
        CEP = self.cleaned_data['CEP']
        if not re.match('^\d{5}-\d{3}', CEP):
            raise forms.ValidationError('CEP inválido')
        return CEP

class PropriedadeEditForm(forms.ModelForm):
    class Meta:
        model = Propriedade
        fields = ['nome', 'descricao', 'imagem']

class ReservaEditForm(forms.ModelForm):
    class Meta:
        model = Reserva

        fields = ['qtd_pessoas']


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

class PagamentoEditForm(forms.ModelForm):
    class Meta:
        model = Pagamento

        fields = ['tipo_pagamento']

    def __init__(self, *args, **kwargs):
        super(PagamentoEditForm, self).__init__(*args, **kwargs)
        self.fields['tipo_pagamento'].label = 'Tipo de pagamento'

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

class BuscaPropForm(forms.Form):
    cidade = forms.CharField(label='Cidade', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    data_ini = forms.DateField(label='Data de entrada', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))
    data_fim = forms.DateField(label='Data de saída', widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}))

    def clean_data_ini(self):
        data_ini = self.cleaned_data['data_ini']
        if data_ini < datetime.date.today():
            raise forms.ValidationError('A data não pode ser no passado')
        return data_ini
    
    def clean_data_fim(self):
        cleaned_data = super().clean()
        data_ini = cleaned_data['data_ini']
        data_fim = cleaned_data['data_fim']
        if data_fim < datetime.date.today():
            raise forms.ValidationError('A data não pode ser no passado')
        if data_fim < data_ini:
            raise forms.ValidationError('Data inválida')
        return data_fim



