from django.contrib import admin
from .models import MealComponent, Ingredient


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


@admin.register(MealComponent)
class MealComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'component_type')
    list_filter = ('component_type',)
    search_fields = ('name', 'description')
    inlines = [IngredientInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('description', 'meal_component')
    search_fields = ('description',)
