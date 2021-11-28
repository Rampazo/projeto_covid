from django.contrib import admin
from .models import Sector


class SectorAdmin(admin.ModelAdmin):
    list_display = ('initial', 'name', 'user_type')


admin.site.register(Sector, SectorAdmin)
