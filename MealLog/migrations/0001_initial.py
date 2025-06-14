# Generated by Django 5.2.1 on 2025-05-27 01:05

import django.db.models.deletion
import django.utils.timezone
import multiselectfield.db.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Diet', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MealLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome da Refeição')),
                ('consumed_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Consumido em')),
                ('meal_type', models.CharField(choices=[('BREAKFAST', 'Café da Manhã'), ('MORNING_SNACK', 'Lanche da Manhã'), ('AFTERNOON_SNACK', 'Lanche da Tarde'), ('SUPPER', 'Ceia'), ('POST_WORKOUT', 'Pós-Treino'), ('OTHER', 'Outro')], max_length=20, verbose_name='Tipo de Refeição')),
                ('is_planned', models.BooleanField(default=False, help_text='Marque se esta refeição faz parte do plano ou foi um consumo esporádico.', verbose_name='Foi Planejado?')),
                ('is_dessert', models.BooleanField(default=False, verbose_name='É sobremesa?')),
                ('description', models.TextField(blank=True, verbose_name='Descrição/Observações')),
                ('diet', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='meal_logs', to='Diet.diet', verbose_name='Plano Alimentar')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meal_logs', to=settings.AUTH_USER_MODEL, verbose_name='Usuário')),
            ],
            options={
                'verbose_name': 'Registro de Refeição',
                'verbose_name_plural': 'Registros de Refeições',
                'ordering': ['-consumed_at'],
            },
        ),
        migrations.CreateModel(
            name='PlannedMeal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Nome do Plano')),
                ('days_of_week', multiselectfield.db.fields.MultiSelectField(choices=[(0, 'Segunda-feira'), (1, 'Terça-feira'), (2, 'Quarta-feira'), (3, 'Quinta-feira'), (4, 'Sexta-feira'), (5, 'Sábado'), (6, 'Domingo')], max_length=13, verbose_name='Dias da Semana')),
                ('meal_type', models.CharField(choices=[('BREAKFAST', 'Café da Manhã'), ('MORNING_SNACK', 'Lanche da Manhã'), ('AFTERNOON_SNACK', 'Lanche da Tarde'), ('SUPPER', 'Ceia'), ('POST_WORKOUT', 'Pós-Treino'), ('OTHER', 'Outro')], max_length=20)),
                ('diet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Diet.diet')),
            ],
        ),
    ]
