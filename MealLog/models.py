from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from multiselectfield import MultiSelectField
from Diet.models import Diet

class MealLog(models.Model):
    """
    Registra uma refeição consumida, seja ela planejada ou esporádica.
    (Substitui o model REFEIÇÃO)
    """
    class MealType(models.TextChoices):
        BREAKFAST = 'BREAKFAST', 'Café da Manhã'
        MORNING_SNACK = 'MORNING_SNACK', 'Lanche da Manhã'
        AFTERNOON_SNACK = 'AFTERNOON_SNACK', 'Lanche da Tarde'
        SUPPER = 'SUPPER', 'Ceia'
        POST_WORKOUT = 'POST_WORKOUT', 'Pós-Treino'
        OTHER = 'OTHER', 'Outro'

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='meal_logs',
        verbose_name="Usuário"
    )
    name = models.CharField(
        max_length=200,
        verbose_name="Nome da Refeição"
    )
    consumed_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="Consumido em"
    )
    meal_type = models.CharField(
        max_length=20,
        choices=MealType.choices,
        verbose_name="Tipo de Refeição"
    )
    is_planned = models.BooleanField(
        default=False,
        verbose_name="Foi Planejado?",
        help_text="Marque se esta refeição faz parte do plano ou foi um consumo esporádico."
    )
    is_dessert = models.BooleanField(
        default=False,
        verbose_name="É sobremesa?"
    )
    diet = models.ForeignKey(
        Diet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='meal_logs',
        verbose_name="Plano Alimentar"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descrição/Observações"
    )

    def __str__(self):
        return f"{self.name} ({self.user.username} em {self.consumed_at.strftime('%d/%m/%y %H:%M')})"

    class Meta:
        verbose_name = "Registro de Refeição"
        verbose_name_plural = "Registros de Refeições"
        ordering = ['-consumed_at']
        
        
class PlannedMeal(models.Model):
    """
    Exemplo de um model para templates de refeições planejadas.
    """
    DAYS_OF_WEEK = (
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    )

    name = models.CharField(
        max_length=200,
        verbose_name="Nome do Plano"
    )
    days_of_week = MultiSelectField(
        choices=DAYS_OF_WEEK,
        max_choices=7,
        verbose_name="Dias da Semana"
    )
    meal_type = models.CharField(
        max_length=20,
        choices=MealLog.MealType.choices
    )
    diet = models.ForeignKey(
        Diet,
        on_delete=models.CASCADE
    )
    
    class Meta:
        verbose_name = "Refeição Planejada"
        verbose_name_plural = "Refeições Planejadas"
    
    def __str__(self):
        return self.name
