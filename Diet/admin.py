from django.contrib import admin
from .models import Diet

@admin.register(Diet)
class DietAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'start_date', 'end_date', 'status')
    list_filter = ('user', 'start_date')
    search_fields = ('name', 'user__username', 'nutritionist_name', 'goal')
    readonly_fields = ('status',)
    autocomplete_fields = ('user',)
