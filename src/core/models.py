from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import uuid
import datetime
# Create your models here.

def get_data():
    return datetime.datetime.now() + datetime.timedelta(days=7)

class Propriedade(models.Model):
    """Representa uma propriedade cadastrada no sistema"""

    # informacoes basicas da propriedade
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="O id unico da propriedade")
    nome = models.CharField(max_length=50, help_text="O nome identificador da propriedade")
    descricao = models.TextField(max_length=500, help_text="Descricao da propriedade")
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    imagem = models.ImageField(upload_to='propriedades/')
    
    # inicio do endereco
    rua = models.CharField(max_length=100, help_text="A rua da propriedade")
    CEP = models.CharField(max_length=100, help_text="O cep da propriedade") # fazer regex para validar
    cidade = models.CharField(max_length=100, help_text="A cidade onde a propriedade se encontra")
    estado = models.CharField(max_length=100, help_text="O estado onde a propriedade se encontra")


    RESERVA_STATUS = (
        ('d', 'disponivel'),
        ('i', 'indisponivel')
    )

    status = models.CharField(
        max_length=1,
        choices=RESERVA_STATUS,
        blank=True,
        default='d',
        help_text="Disponibilidade para reserva"
    )

    def __str__(self):
        """Representacao da propriedade em string"""
        return self.nome

    def get_id(self):
        return str(self.id)



class Reserva(models.Model):
    """Representa uma reserva cadastrada no sistema"""
    hospede = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.PROTECT, blank=True)
    dados_pagamento = models.ForeignKey('Pagamento', on_delete=models.PROTECT, blank=True)

    qtdPessoas = models.IntegerField('Quantidade de pessoas da reserva', default=1)
    ini = models.DateField('Inicio da reserva', default=datetime.datetime.now)
    fim = models.DateField('Fim da reserva', default=get_data)

    def __str__(self):
        """Representacao da reserva em string"""
        return self.propriedade.nome

class Pagamento(models.Model):
    """Representa o pagamento de uma reserva existente no sistema"""
    id_transacao = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="O id unico da transacao")

    ESCOLHAS_PAGAMENTO = (
        ('Débito', 'Débito'),
        ('Crédito', 'Crédito')
    )
    
    tipo_pagamento = models.CharField(
        max_length=7,
        choices=ESCOLHAS_PAGAMENTO,
        blank=False,
        default='Crédito',
        help_text='Tipo de pagamento'
    )

    PAGAMENTO_STATUS = (
        ('C', 'concluido'),
        ('I', 'inconcluido')
    )

    status = models.CharField(
        max_length=1,
        choices=PAGAMENTO_STATUS,
        blank=True,
        default='C',
        help_text="Status do pagamento"
    )

    def __str__(self):
        return f'{self.id_transacao} ({self.status})'