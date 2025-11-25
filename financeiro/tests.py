from rest_framework.test import APITestCase
from rest_framework import status
from .models import Lancamento
from datetime import date

class LancamentoAPITest(APITestCase):
    
    def setUp(self):
        self.receita = Lancamento.objects.create(
            descricao="Salário Mensal",
            valor=5000.00,
            data=date(2025, 11, 1),
            tipo="RECEITA",
            categoria="Trabalho"
        )
        self.despesa = Lancamento.objects.create(
            descricao="Conta de Luz",
            valor=200.00,
            data=date(2025, 11, 10),
            tipo="DESPESA",
            categoria="Casa"
        )
        self.id_receita = self.receita.id


    def test_deve_filtrar_por_tipo(self):
        """Verifica se ?tipo=RECEITA traz apenas receitas"""
        url = '/api/lancamentos/?tipo=RECEITA'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1) # Só deve vir o Salário
        self.assertEqual(response.data[0]['tipo'], 'RECEITA')

    def test_deve_buscar_por_texto(self):
        """Verifica se ?search=Luz encontra a conta de luz"""
        url = '/api/lancamentos/?search=Luz'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['descricao'], "Conta de Luz")

    def test_deve_ordenar_por_valor_decrescente(self):
        """Verifica se ?ordering=-valor traz o mais caro primeiro"""
        url = '/api/lancamentos/?ordering=-valor'
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data[0]['valor']), 5000.00)

    def test_deve_listar_lancamentos(self):
        response = self.client.get('/api/lancamentos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2) # Temos 2 itens no banco

    def test_deve_criar_lancamento(self):
        dados = {
            "descricao": "Internet", "valor": "100.00", 
            "data": "2025-11-15", "tipo": "DESPESA"
        }
        response = self.client.post('/api/lancamentos/', dados)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lancamento.objects.count(), 3)

    def test_deve_atualizar_lancamento(self):
        url = f'/api/lancamentos/{self.id_receita}/'
        novos_dados = {
            "descricao": "Salário com Aumento", "valor": "6000.00",
            "data": "2025-11-01", "tipo": "RECEITA"
        }
        response = self.client.put(url, novos_dados)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.receita.refresh_from_db()
        self.assertEqual(self.receita.valor, 6000.00)

    def test_deve_deletar_lancamento(self):
        url = f'/api/lancamentos/{self.id_receita}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lancamento.objects.count(), 1)

    def test_nao_deve_aceitar_valor_negativo(self):
        dados = { "descricao": "Erro", "valor": "-50.00", "data": "2025-01-01", "tipo": "DESPESA" }
        response = self.client.post('/api/lancamentos/', dados)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deve_gerar_relatorio_csv(self):
        response = self.client.get('/api/lancamentos/exportar_csv/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'text/csv')

    def test_deve_gerar_relatorio_pdf(self):
        response = self.client.get('/api/lancamentos/exportar_pdf/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get('Content-Type'), 'application/pdf')