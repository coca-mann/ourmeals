from django.contrib import admin
from .models import MealPrep, MealComponent, Ingredient, MealPrepComponent


class IngredientInline(admin.TabularInline):
    """Permite adicionar Ingredientes diretamente na página do MealComponent."""
    model = Ingredient
    extra = 1


class MealPrepComponentInline(admin.TabularInline):
    """Permite adicionar Componentes diretamente na página do MealPrep."""
    model = MealPrepComponent
    extra = 1
    autocomplete_fields = ('component', 'user')


@admin.register(MealComponent)
class MealComponentAdmin(admin.ModelAdmin):
    """Admin para o catálogo de "Misturas" (Componentes)."""
    list_display = ('name', 'component_type')
    list_filter = ('component_type',)
    search_fields = ('name', 'description')
    inlines = [IngredientInline]


@admin.register(MealPrep)
class MealPrepAdmin(admin.ModelAdmin):
    """Admin para o planejamento das "Marmitas" (MealPrep)."""
    list_display = ('name', 'target_date', 'meal_type', 'is_prepared')
    list_filter = ('is_prepared', 'meal_type', 'target_date')
    search_fields = ('name', 'notes')
    date_hierarchy = 'target_date'
    filter_horizontal = ('intended_for',)
    inlines = [MealPrepComponentInline]
    exclude = ('components',)


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('description', 'meal_component')
    search_fields = ('description',)
    autocomplete_fields = ('meal_component',)


@admin.register(MealPrepComponent)
class MealPrepComponentAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'meal_prep', 'component', 'user', 'quantity', 'unit_of_measure')
    list_filter = ('meal_prep', 'component', 'user')
    autocomplete_fields = ('meal_prep', 'component', 'user')