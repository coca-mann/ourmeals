from django.contrib import admin
from .models import MealLog, PlannedMeal

@admin.register(MealLog)
class MealLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'consumed_at', 'meal_type', 'is_planned')
    list_filter = ('user', 'meal_type', 'is_planned')
    search_fields = ('name', 'description', 'user__username')
    date_hierarchy = 'consumed_at'
    autocomplete_fields = ('user', 'diet')


@admin.register(PlannedMeal)
class PlannedMealAdmin(admin.ModelAdmin):
    list_display = ('name', 'diet', 'meal_type', 'display_days_of_week')
    list_filter = ('diet', 'meal_type', 'days_of_week')
    search_fields = ('name', 'diet__name')
    autocomplete_fields = ('diet',)

    def display_days_of_week(self, obj):
        if not obj.days_of_week:
            return "Nenhum dia selecionado"
        
        day_map = dict(obj.DAYS_OF_WEEK)
        return ", ".join(day_map.get(int(day)) for day in obj.days_of_week)
    
    display_days_of_week.short_description = 'Dias da Semana'
