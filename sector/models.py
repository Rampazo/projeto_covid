from django.db import models


class Sector(models.Model):

    USER_TYPE_CHOICES = [
        ('Estudante', 'Estudante'),
        ('Funcionario', 'Funcionario'),
        ('Gestor', 'Gestor'),
        ('Professor', 'Professor'),
        ('RH', 'Recursos Humanos')
    ]

    name = models.CharField(max_length=200, verbose_name='Nome')
    initial = models.CharField(max_length=5, verbose_name='Sigla')
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, verbose_name='Tipo de Usuário')
    active = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'

    def __str__(self):
        return f'{self.initial} - {self.name}'
