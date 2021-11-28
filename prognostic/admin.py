from django.contrib import admin
from .models import Prognostic


class PrognosticAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'active')


admin.site.register(Prognostic, PrognosticAdmin)
