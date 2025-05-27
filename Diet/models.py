import datetime
from django.db import models
from django.contrib.auth.models import User

class Diet(models.Model):
    """
    Representa um plano alimentar (dieta) com um período e objetivo definidos.
    """
    name = models.CharField(
        max_length=200,
        verbose_name="Nome da Dieta"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='diets',
        verbose_name="Usuário"
    )
    start_date = models.DateField(
        verbose_name="Data de Início"
    )
    end_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Data de Fim",
        help_text="Deixe em branco se a dieta não tiver um prazo definido."
    )
    nutritionist_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Nutricionista/Clínica"
    )
    goal = models.TextField(
        blank=True,
        verbose_name="Objetivo",
        help_text="Ex: Perda de peso, ganho de massa, reeducação alimentar."
    )
    attachment = models.FileField(
        upload_to='diets/',
        blank=True,
        null=True,
        verbose_name="Anexo",
        help_text="Anexe o arquivo PDF ou imagem original da dieta."
    )
    
    @property
    def status(self):
        if not self.start_date:
            return "Pendente"
        today = datetime.date.today()
        if self.start_date > today:
            return "Planejada"
        if self.end_date is None or self.end_date >= today:
            return "Ativa"
        return "Concluída"

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    class Meta:
        verbose_name = "Plano Alimentar"
        verbose_name_plural = "Planos Alimentares"
        ordering = ['-start_date', 'user']
