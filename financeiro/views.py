from django.shortcuts import render

from rest_framework import viewsets
from .models import Lancamento
from .serializers import LancamentoSerializer

class LancamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar Lançamentos.
    Fornece automaticamente as ações: list, create, retrieve, update e destroy.
    """
    queryset = Lancamento.objects.all()
    serializer_class = LancamentoSerializer