from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from .forms import *
import uuid
import datetime

# Classe que executa testes em um Model do tipo Propriedade
class TestPropriedade(TestCase):
    def setUp(self):
        # Criação da propriedade
        User.objects.create_user(
            'andrew',
            'andrew@nap.com',
            'FccRX*tJ'
        )
        self.usuario = User.objects.get(username='andrew')
        self.id = uuid.uuid4()
        Propriedade.objects.create(
            id = self.id,
            nome = 'Casa assombrada',
            descricao = 'Casa com 12 cômodos. Grande, feia, solitária. Odiada até pelos fantasmas que vivem nela...',
            proprietario = self.usuario,
            imagem = 'boo.jpg',
            rua = 'Rua do Mal, 11',
            CEP = '66666-666',
            cidade = 'Manaus',
            estado = 'AM'
        )
        self.propriedade = Propriedade.objects.get(id = self.id)
    
    # Testa o ID da propriedade
    def test_id(self):
        self.assertEqual(self.propriedade.id, self.id)

    # Testa o nome da propriedade
    def test_nome(self):
        self.assertEqual(self.propriedade.nome, 'Casa assombrada')
    
    # Testa o proprietário da propriedade
    def test_proprietario(self):
        self.assertEqual(self.propriedade.proprietario, self.usuario)
    
    # Testa se caminho da imagem da propriedade
    def test_imagem(self):
        self.assertEqual(self.propriedade.imagem, 'boo.jpg')
    
    # Testa a rua da propriedade
    def test_rua(self):
        self.assertEqual(self.propriedade.rua, 'Rua do Mal, 11')
    
    # Testa o CEP da propriedade
    def test_CEP(self):
        self.assertEqual(self.propriedade.CEP, '66666-666')

    # Testa a cidade da propriedade
    def test_cidade(self):
        self.assertEqual(self.propriedade.cidade, 'Manaus')

    # Testa o estado da Propriedade
    def test_estado(self):
        self.assertEqual(self.propriedade.estado, 'AM')

# Classe que executa testes em um Model do tipo Pagamento
class TestPagamento(TestCase):
    def setUp(self):
        # Criação do pagamento
        self.id_transacao = uuid.uuid4()
        Pagamento.objects.create(
            id_transacao = self.id_transacao,
            tipo_pagamento = 'Crédito',
            status = 'C'
        )
        self.pagamento = Pagamento.objects.get(id_transacao = self.id_transacao)
    # Testa o ID da transação
    def test_id_transacao(self):
        self.assertEqual(self.pagamento.id_transacao, self.id_transacao)
    
    # Testa o tipo de pagamento
    def test_tipo_pagamento(self):
        self.assertEqual(self.pagamento.tipo_pagamento, 'Crédito')

    # Testa o status do pagamento
    def test_status(self):
        self.assertEqual(self.pagamento.status, 'C')

# Classe que executa testes em um Model do tipo Reserva
class TestReserva(TestCase):
    def setUp(self):
        # Criação da propriedade
        User.objects.create_user(
            'andrew',
            'andrew@nap.com',
            'FccRX*tJ'
        )
        self.proprietario = User.objects.get(username='andrew')
        self.id = uuid.uuid4()
        Propriedade.objects.create(
            id = self.id,
            nome = 'Casa assombrada',
            descricao = 'Casa com 12 cômodos. Grande, feia, solitária. Odiada até pelos fantasmas que vivem nela...',
            proprietario = self.proprietario,
            imagem = 'boo.jpg',
            rua = 'Rua do Mal, 11',
            CEP = '66666-666',
            cidade = 'Manaus',
            estado = 'AM'
        )
        self.propriedade = Propriedade.objects.get(id = self.id)

        # Criação do hóspede
        User.objects.create_user(
            'juli',
            'juli@hotmail.com',
            'h&34a*tJ'
        )
        self.hospede = User.objects.get(username='juli')

        # Criação do Pagamento
        self.id_transacao = uuid.uuid4()
        Pagamento.objects.create(
            id_transacao = self.id_transacao,
            tipo_pagamento = 'Crédito',
            status = 'C'
        )
        self.pagamento = Pagamento.objects.get(id_transacao = self.id_transacao)

        # Criação da reserva
        self.id_reserva = uuid.uuid4()
        self.data_ini = datetime.datetime.now()
        self.data_fim = datetime.datetime.now() + datetime.timedelta(days=7)
        Reserva.objects.create(
            id = self.id_reserva,
            hospede = self.hospede,
            propriedade = self.propriedade,
            dados_pagamento = self.pagamento,
            qtd_pessoas = '1',
            dini = self.data_ini,
            dfim = self.data_fim
        )
        self.reserva = Reserva.objects.get(id = self.id_reserva)

    # Testa o ID da reserva
    def test_id(self):
        self.assertEqual(self.reserva.id, self.id_reserva)

    # Testa o hóspede da reserva
    def test_hospede(self):
        self.assertEqual(self.reserva.hospede, self.hospede)

    # Testa a propriedade da reserva
    def test_propriedade(self):
        self.assertEqual(self.reserva.propriedade, self.propriedade)
    
    # Testa os dados de pagamento da reserva
    def test_dados_pagamento(self):
        self.assertEqual(self.reserva.dados_pagamento, self.pagamento)

    # Testa a quantidade de pessoas da reserva
    def test_qtd_pessoas(self):
        self.assertEqual(self.reserva.qtd_pessoas, '1')

    # Testa a data inicial da reserva
    def test_dini(self):
        # Convertendo a data existente no objeto para um objeto do tipo string
        # E também a data presente na classe para poder executar a comparação
        # Caso contrário, o teste falharia, pois datetime.datetime.now()
        # Fornece uma data com hora, minuto, segundos, etc...
        # E a data presente em Reserva não contém esses campos mais
        self.assertEqual(self.reserva.dini.strftime("%Y-%m-%d"), self.data_ini.strftime("%Y-%m-%d"))

    # Testa a data final da reserva
    def test_dfim(self):
        # Convertendo a data existente no objeto para um objeto do tipo string
        # E também a data presente na classe para poder executar a comparação
        # Caso contrário, o teste falharia, pois datetime.datetime.now()
        # Fornece uma data com hora, minuto, segundos, etc...
        # E a data presente em Reserva não contém esses campos mais
        self.assertEqual(self.reserva.dfim.strftime("%Y-%m-%d"), self.data_fim.strftime("%Y-%m-%d"))

# Classe que testa se a validação feita no formulário
# BuscaPropriedade é realizada corretamente
class TestBuscaPropriedadeForm(TestCase):
    def setUp(self):
        self.cidade = 'Lavras'
        self.data_ini_invalido = datetime.datetime.strptime("2018-08-27", "%Y-%m-%d")
        self.data_fim_invalido = datetime.datetime.strptime("2016-08-27", "%Y-%m-%d")
        self.data_ini = datetime.datetime.strptime("2020-01-01", "%Y-%m-%d")
        self.data_fim = datetime.datetime.strptime("2020-01-15", "%Y-%m-%d")

    # Testa se o form não possui erros ao ser fornecido um dado válido
    def test_form_valido(self):
        dados = {
            'cidade': self.cidade,
            'data_ini': self.data_ini,
            'data_fim': self.data_fim
        }
        form = BuscaPropForm(data = dados)
        self.assertTrue(form.is_valid())
    
    # Testa se o form possui erros ao ser fornecido um dado inválido
    def test_form_invalido(self):
        dados = {
            'cidade': self.cidade,
            'data_ini': self.data_ini_invalido,
            'data_fim': self.data_fim_invalido
        }
        form = BuscaPropForm(data = dados)
        self.assertFalse(form.is_valid())

# Classe que testa se a validação interna feita no formulário
# RegistrarForm é realizada corretamente
class TestRegistrarForm(TestCase):
    def setUp(self):
        self.usuario = 'andrew'
        self.password1 = 'abacaxi1234'
        self.password2 = 'abacaxi12345'
        self.email = 'andrew@email.com'
        self.email_invalido = 'andrewemail.com'
        self.prim_nome = 'Andrew'
        self.ult_nome = 'Werdna'

    # Testa se o form não possui erros ao ser fornecido um dado válido
    def test_form_valido(self):
        dados = {
            'username': self.usuario,
            'password1': self.password1,
            'password2': self.password1,
            'email': self.email,
            'first_name': self.prim_nome,
            'last_name': self.ult_nome
        }
        form = RegistrarForm(data=dados)
        self.assertTrue(form.is_valid())

    # Testa se o form possui erros ao ser fornecido um dado inválido
    def test_form_invalido(self):
        dados = {
            'username': self.usuario,
            'password1': self.password1,
            'password2': self.password2,
            'email': self.email_invalido,
            'first_name': self.prim_nome,
            'last_name': self.ult_nome
        }
        form = RegistrarForm(data=dados)
        self.assertFalse(form.is_valid())
