from django.db import models
from django.contrib.auth.models import User


class MealPrep(models.Model):
    """
    Represents a batch of prepared meals (marmitas) for the week.
    """
    class MealType(models.TextChoices):
        LUNCH = 'LUNCH', 'Almoço'
        DINNER = 'DINNER', 'Janta'

    name = models.CharField(
        max_length=200,
        verbose_name="Nome da Marmita"
    )
    # Sugestão 1: Unificar 'Semana' e 'Mes/Ano' em um único campo de data.
    target_date = models.DateField(
        verbose_name="Data Planejada",
        help_text="Data para a qual a marmita está planejada. Usada para agrupar por semana ou mês."
    )
    components = models.ManyToManyField(
        'MealComponent',
        through='MealPrepComponent', # Especificando que a ligação se dá pelo nosso novo model
        verbose_name="Componentes"
    )
    meal_type = models.CharField(
        max_length=10,
        choices=MealType.choices,
        verbose_name="Tipo de Refeição"
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name="Quantidade a Fazer"
    )
    is_prepared = models.BooleanField(
        default=False,
        verbose_name="Já foi feita?"
    )
    diet = models.ForeignKey(
        'Diet', # Assume que o model se chamará 'Diet'
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meal_preps',
        verbose_name="Plano Alimentar"
    )
    notes = models.TextField(
        blank=True,
        verbose_name="Observações"
    )
    
    # --- NOVOS CAMPOS SUGERIDOS ---
    
    # Sugestão 2: Registrar para quem são as marmitas.
    intended_for = models.ManyToManyField(
        User,
        related_name='meal_preps',
        verbose_name="Destinado para",
        help_text="Selecione para quem são estas marmitas."
    )
    
    # Sugestão 3: Registrar quando a preparação foi realmente feita.
    prepared_on = models.DateField(
        null=True,
        blank=True,
        verbose_name="Data da Preparação"
    )

    def __str__(self):
        return f"{self.name} ({self.get_meal_type_display()} - {self.target_date.strftime('%d/%m/%Y')})"

    class Meta:
        verbose_name = "Marmita Planejada"
        verbose_name_plural = "Marmitas Planejadas"
        ordering = ['-target_date']