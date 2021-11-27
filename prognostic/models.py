from django.db import models


class Prognostic(models.Model):

    name = models.CharField(max_length=200, verbose_name='Nome')
    description = models.CharField(max_length=200, verbose_name='Descrição')
    active = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Prognóstico'
        verbose_name_plural = 'Prognósticos'

    def __str__(self):
        return self.name

    # def save(self, *args, **kwargs):
    #     print(self.name)
    #     super(Prognostic, self).save(*args, **kwargs)
