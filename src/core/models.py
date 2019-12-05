from django.db import models
from django.contrib.auth.models import User

import uuid
import datetime

# Função auxiliar para definir o tempo default
# De uma reserva
def get_data():
    return datetime.datetime.now() + datetime.timedelta(days=7)

# Classe para o model Propriedade, com campos que descrevem
# Uma propriedade em um sistema de reservas
class Propriedade(models.Model):

    # informacoes basicas da propriedade
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='O id unico da propriedade')
    nome = models.CharField(max_length=50, help_text='O nome da propriedade')
    descricao = models.TextField(max_length=500, help_text='Descrição da propriedade')
    proprietario = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    imagem = models.ImageField(upload_to='propriedades/', help_text='Imagem identificadora da propriedade')
    
    # inicio do endereco
    rua = models.CharField(max_length=100, help_text='A rua da propriedade')
    CEP = models.CharField(max_length=100, help_text='O CEP da propriedade') # fazer regex para validar
    cidade = models.CharField(max_length=100, help_text='A cidade onde a propriedade se encontra')

    # as possíveis escolhas para o campo estado
    ESTADO_CHOICES = (
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espirito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )

    estado = models.CharField(max_length=2, choices=ESTADO_CHOICES, help_text='O estado onde a propriedade se encontra')

    def __str__(self):
        return self.nome

    def get_id(self):
        return str(self.id)


# Classe para o model Reserva, com campos que descrevem
# Uma reserva em um sistema de reservas
class Reserva(models.Model):

    # informacoes basicas da reserva
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    hospede = models.ForeignKey(User, on_delete=models.PROTECT, blank=True)
    propriedade = models.ForeignKey(Propriedade, on_delete=models.PROTECT, blank=True)
    dados_pagamento = models.ForeignKey('Pagamento', on_delete=models.PROTECT, blank=True)

    # as possiveis escolhas para o campo qtd_pessoas
    QTD_PESSOAS_CHOICES = (
        ('1', '1 pessoa'),
        ('2', '2 pessoas'),
        ('3', '3 pessoas'),
    )

    qtd_pessoas = models.CharField('Quantidade de pessoas da reserva', max_length=1, choices=QTD_PESSOAS_CHOICES, default=1)

    # campos do tipo data, que determinam o inicio e o fim da reserva
    dini = models.DateField('Inicio da reserva', default=datetime.datetime.now)
    dfim = models.DateField('Fim da reserva', default=get_data)

    def __str__(self):
        return self.propriedade.nome

# Classe para o model Pagamento, com campos que descrevem
# Um pagamento em um sistema de reservas
class Pagamento(models.Model):

    # informacoes basicas do pagamento
    id_transacao = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='O id unico da transacao')

    # variavel que determina as possiveis escolhas para o campo
    # tipo_pagamento
    ESCOLHAS_PAGAMENTO = (
        ('Débito', 'Débito'),
        ('Crédito', 'Crédito')
    )
    
    tipo_pagamento = models.CharField(
        max_length=7,
        choices=ESCOLHAS_PAGAMENTO,
        default='Crédito',
        help_text='Tipo de pagamento'
    )
    
    # variavel que determina as possiveis escolhas para o campo
    # status
    PAGAMENTO_STATUS = (
        ('C', 'concluido'),
        ('I', 'inconcluido')
    )

    status = models.CharField(
        max_length=1,
        choices=PAGAMENTO_STATUS,
        default='C',
        help_text='Status do pagamento'
    )

    def __str__(self):
        return f'{self.id_transacao} ({self.status})'