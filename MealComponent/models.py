from django.db import models

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
