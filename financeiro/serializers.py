from rest_framework import serializers
from  .models import Lancamento
from datetime import date

class LancamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lancamento
        fields = '__all__'

    #validação para valores negativos ou zero
    def validate_valor(self, value):
        if value <= 0:
            raise serializers.ValidationError("O valor não deve ser negativo ou zero")
        return value

    #validação pde data futura
    def validate_data(self, value):
        if value > date.today():
            raise serializers.ValidationError("A data não pode ser futura")
        return value

