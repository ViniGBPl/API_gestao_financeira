import csv
from django.http import HttpResponse
from django.db.models import Sum
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from .models import Lancamento
from .serializers import LancamentoSerializer

# O 'extend_schema_view' serve para modificar métodos padrões do Django (como o 'list')
@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                name='ordering',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Selecione a ordenação dos resultados:',
                # AQUI ESTÁ O SEGREDOS: Definimos a lista exata de opções
                enum=['data', '-data', 'valor', '-valor', 'descricao', '-descricao'],
            ),
        ]
    )
)
class LancamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet completo com CRUD, Filtros, Relatórios e Documentação Avançada.
    """
    queryset = Lancamento.objects.all()
    serializer_class = LancamentoSerializer
    
    # Filtros do Backend 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tipo', 'categoria', 'data']
    search_fields = ['descricao']
    ordering_fields = ['data', 'valor', 'descricao'] # Campos permitidos

    # RELATÓRIO DE SALDO
    @extend_schema(
        parameters=[
            OpenApiParameter("mes", OpenApiTypes.INT, description="Mês (1-12)", required=True),
            OpenApiParameter("ano", OpenApiTypes.INT, description="Ano (ex: 2025)", required=True),
        ],
        description="Retorna o saldo consolidado do mês."
    )
    @action(detail=False, methods=['get'])
    def saldo_mensal(self, request):
        mes = request.query_params.get('mes')
        ano = request.query_params.get('ano')

        if not mes or not ano:
            return Response({"erro": "Informe 'mes' e 'ano'."}, status=400)

        lancamentos = self.queryset.filter(data__month=mes, data__year=ano)
        receitas = lancamentos.filter(tipo='RECEITA').aggregate(Sum('valor'))['valor__sum'] or 0
        despesas = lancamentos.filter(tipo='DESPESA').aggregate(Sum('valor'))['valor__sum'] or 0
        
        return Response({
            "mes": mes, "ano": ano,
            "receitas": receitas,
            "despesas": despesas,
            "saldo": receitas - despesas
        })

    # EXPORTAÇÃO CSV 
    @action(detail=False, methods=['get'])
    def exportar_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="extrato.csv"'

        writer = csv.writer(response)
        writer.writerow(['ID', 'Data', 'Descrição', 'Tipo', 'Valor', 'Categoria'])
        dados = self.filter_queryset(self.get_queryset())

        for item in dados:
            writer.writerow([item.id, item.data, item.descricao, item.tipo, item.valor, item.categoria])
        return response

    # EXPORTAÇÃO PDF
    @action(detail=False, methods=['get'])
    def exportar_pdf(self, request):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="extrato_financeiro.pdf"'

        p = canvas.Canvas(response, pagesize=A4)
        width, height = A4
        
        # Cabeçalho
        p.setFillColor(colors.darkblue)
        p.rect(0, height - 80, width, 80, fill=True, stroke=False)
        p.setFillColor(colors.white)
        p.setFont("Helvetica-Bold", 24)
        p.drawString(30, height - 50, "Extrato Financeiro")
        p.setFont("Helvetica", 12)
        p.drawString(30, height - 70, "Relatório Automático")

        # Tabela
        y = height - 120
        p.setFillColor(colors.black)
        p.setFont("Helvetica-Bold", 10)
        p.drawString(30, y, "DATA"); p.drawString(100, y, "DESCRIÇÃO"); 
        p.drawString(300, y, "CATEGORIA"); p.drawString(400, y, "TIPO"); p.drawString(500, y, "VALOR")
        p.line(30, y - 5, width - 30, y - 5)
        y -= 25

        dados = self.filter_queryset(self.get_queryset())
        p.setFont("Helvetica", 10)

        for item in dados:
            if y < 50: p.showPage(); y = height - 50
            
            p.setFillColor(colors.black)
            p.drawString(30, y, str(item.data.strftime("%d/%m/%Y")))
            p.drawString(100, y, item.descricao[:35])
            p.drawString(300, y, str(item.categoria or "-"))
            p.setFillColor(colors.green if item.tipo == 'RECEITA' else colors.red)
            p.drawString(400, y, item.tipo)
            p.drawString(500, y, f"R$ {item.valor}")
            p.setStrokeColor(colors.lightgrey)
            p.line(30, y - 5, width - 30, y - 5)
            y -= 20

        p.save()
        return response