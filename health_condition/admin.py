from django import forms
from django.contrib import admin, messages
from django.core.exceptions import ValidationError

from .models import HealthCondition
from user.models import UserProfile


class HealthConditionForm(forms.ModelForm):
    class Meta:
        model = HealthCondition
        fields = ['user_id', 'health_state', 'prognostic_id', 'create_at']

    def clean(self):
        health_state = self.cleaned_data.get('health_state')
        prognostic_id = self.cleaned_data.get('prognostic_id')

        if health_state == 'YES' and prognostic_id:
            raise ValidationError('Não é possível cadastrar prognóticos quando o Estado de Saúde é "Bem"')
        elif health_state == 'NO' and not prognostic_id:
            raise ValidationError('Não é possível não cadastrar prognóticos quando o Estado de Saúde é "Não muito bem"')
        else:
            return self.cleaned_data


class HealthConditionAdmin(admin.ModelAdmin):
    filter_horizontal = ('prognostic_id',)
    form = HealthConditionForm
    list_display = ('get_user_name', 'health_state', 'create_at')
    readonly_fields = ('create_at',)

    @admin.display(ordering='user_id__name', description='Nome')
    def get_user_name(self, obj):
        return obj.user_id.name

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user_id':
            if request.user.id not in [1, 89]:
                user_profile = UserProfile.objects.get(user_id=request.user.id)
                kwargs['initial'] = user_profile.id
                kwargs['disabled'] = True
        if db_field.name == 'create_at':
            kwargs['disabled'] = True
        return super(HealthConditionAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_list_display(self, request):
        if request.user.id not in [1, 89]:
            user_profile = UserProfile.objects.get(user_id=request.user.id)
            request.environ['QUERY_STRING'] = f'user_id__id__exact={user_profile.id}'
        return super(HealthConditionAdmin, self).get_list_display(request)

    def save_model(self, request, obj, form, change):
        if obj.health_state == 'YES':
            messages.add_message(request, messages.INFO, 'Agradecemos por colaborar com suas informações!')
        elif obj.health_state == 'NO':
            messages.add_message(request, messages.WARNING, """ATENÇÃO! Procure orientações por meio de um canal oficial 
            do serviço de saúde.\n Secretaria de Atenção Primária à Saúde disponibiliza os canais do TeleSUS - 
            https://aps.saude.gov.br/ape/corona/telesus""")
        super(HealthConditionAdmin, self).save_model(request, obj, form, change)


admin.site.register(HealthCondition, HealthConditionAdmin)

