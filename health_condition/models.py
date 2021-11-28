import json

from datetime import datetime
from django.db import models
from django.core.exceptions import ValidationError

from user.models import UserProfile
from prognostic.models import Prognostic


class HealthCondition(models.Model):

    HEALTH_STATES = [
        ('YES', 'Bem'),
        ('NO', 'Não muito bem')
    ]

    user_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='Usuário')
    health_state = models.CharField(max_length=13, choices=HEALTH_STATES, verbose_name='Estado de Saúde')
    prognostic_id = models.ManyToManyField(Prognostic, verbose_name='Prognósticos', blank=True)
    create_at = models.DateTimeField(verbose_name="Data de Criação", default=datetime.now(), editable=False)

    class Meta:
        verbose_name = 'Condição de Saúde'
        verbose_name_plural = 'Condições de Saúde'

    def __str__(self):
        return self.user_id.name

    def set_prognostic(self, x):
        self.prognostic = json.dumps(x)

    def get_prognostic(self):
        return json.loads(self.prognostic)
