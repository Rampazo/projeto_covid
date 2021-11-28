from django.contrib import admin
from .models import DailyQuantity, DailyQuantityBad, DailyQuantityBadBySector, DailyQuantityBySector, PeopleQuantityBadLastFiveDays


class DailyQuantityAdmin(admin.ModelAdmin):
    list_display = ('initial_date', 'end_date')


class DailyQuantityBadAdmin(admin.ModelAdmin):
    list_display = ('initial_date', 'end_date')


class DailyQuantityBySectorAdmin(admin.ModelAdmin):
    list_display = ('initial_date', 'end_date')


class DailyQuantityBadBySectorAdmin(admin.ModelAdmin):
    list_display = ('initial_date', 'end_date')


admin.site.register(DailyQuantity, DailyQuantityAdmin)
admin.site.register(DailyQuantityBad, DailyQuantityBadAdmin)
admin.site.register(DailyQuantityBySector, DailyQuantityBySectorAdmin)
admin.site.register(DailyQuantityBadBySector, DailyQuantityBadBySectorAdmin)
admin.site.register(PeopleQuantityBadLastFiveDays)
