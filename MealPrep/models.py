from django.db import models
from django.contrib.auth.models import User
from Diet.models import Diet

class MealComponent(models.Model):
    """
    Represents a food component (mistura) that can be part of a MealPrep.
    Ex: Arroz, Frango ao molho, Legumes.
    """
    class ComponentType(models.TextChoices):
        PROTEIN = 'PROTEIN', 'Proteína'
        CARBOHYDRATE = 'CARBOHYDRATE', 'Carboidrato'
        VEGETABLE = 'VEGETABLE', 'Vegetal/Legume'
        SAUCE = 'SAUCE', 'Molho'
        OTHER = 'OTHER', 'Outro'

    name = models.CharField(
        max_length=150,
        verbose_name="Nome do Componente"
    )
    component_type = models.CharField(
        max_length=20,
        choices=ComponentType.choices,
        verbose_name="Tipo de Componente"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Modo de Preparo/Descrição"
    )
    photo = models.ImageField(
        upload_to='components/',
        blank=True,
        null=True,
        verbose_name="Foto"
    )
    calories_per_serving = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="Calorias por porção"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Componente da Refeição"
        verbose_name_plural = "Componentes da Refeição"


class Ingredient(models.Model):
    """
    Represents a single ingredient required for a MealComponent.
    """
    meal_component = models.ForeignKey(
        MealComponent,
        on_delete=models.CASCADE,
        related_name='ingredients', # Permite acessar os ingredientes a partir de um MealComponent
        verbose_name="Componente da Refeição"
    )
    description = models.CharField(
        max_length=255,
        verbose_name="Descrição do Ingrediente",
        help_text="Ex: 1.5kg de bife de patinho, 2 cebolas grandes"
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = "Ingrediente"
        verbose_name_plural = "Ingredientes"


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
    target_date = models.DateField(
        verbose_name="Data Planejada",
        help_text="Data para a qual a marmita está planejada. Usada para agrupar por semana ou mês."
    )
    components = models.ManyToManyField(
        MealComponent,
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
        Diet,
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
    intended_for = models.ManyToManyField(
        User,
        related_name='meal_preps',
        verbose_name="Destinado para",
        help_text="Selecione para quem são estas marmitas."
    )
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


class MealPrepComponent(models.Model):
    """
    Modelo 'through' que conecta uma MealPrep a um MealComponent,
    especificando a quantidade, unidade e o usuário para essa porção.
    """
    class UnitOfMeasure(models.TextChoices):
        GRAMS = 'g', 'Gramas'
        MILLILITERS = 'ml', 'Mililitros'
        UNIT = 'un', 'Unidade(s)'
        SPOON = 'colher', 'Colher(es)'

    meal_prep = models.ForeignKey(
        MealPrep,
        on_delete=models.CASCADE
    )
    component = models.ForeignKey(
        MealComponent,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuário"
    )
    quantity = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Quantidade"
    )
    unit_of_measure = models.CharField(
        max_length=10,
        choices=UnitOfMeasure.choices,
        default=UnitOfMeasure.GRAMS,
        verbose_name="Unidade de Medida"
    )
    notes = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Observações",
        help_text="Ex: um pouco mais apimentado, sem sal, etc."
    )

    class Meta:
        verbose_name = "Componente da Marmita"
        verbose_name_plural = "Componentes das Marmitas"
        unique_together = ('meal_prep', 'component', 'user')

    def __str__(self):
        return f"{self.quantity}{self.unit_of_measure} de {self.component.name} para {self.user.username}"
