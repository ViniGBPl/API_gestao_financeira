from django.db import models

class Lancamento(models.Model):
    # Tuplas para limitar as opções no banco de dados (e no dropdown do Admin)
    TIPO_CHOICES = [
        ('RECEITA', 'Receita'),
        ('DESPESA', 'Despesa'),
    ]

    descricao = models.CharField(max_length=100, verbose_name="Descrição")
    
    # IMPORTANTE: DecimalField é obrigatório para dinheiro. Float tem imprecisão.
    # max_digits=10, decimal_places=2 permite valores até 99.999.999,99
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor")
    
    data = models.DateField(verbose_name="Data do Lançamento")
    
    tipo = models.CharField(max_length=7, choices=TIPO_CHOICES, verbose_name="Tipo")
    
    # Campo opcional para categorizar (ex: Alimentação, Transporte)
    categoria = models.CharField(max_length=50, blank=True, null=True, verbose_name="Categoria")
    
    # Auditoria: salva automaticamente quando o registro foi criado
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        verbose_name = "Lançamento"
        verbose_name_plural = "Lançamentos"
        ordering = ['-data'] # Exibe primeiro os lançamentos mais recentes

    def __str__(self):
        # Isso define como o objeto aparece no painel do Django Admin
        return f"{self.descricao} - R$ {self.valor}"