from django.contrib import admin
from .models import DailyQuantity, DailyQuantityBad, DailyQuantityBadBySector, DailyQuantityBySector, PeopleQuantityBadLastFiveDays

admin.site.register(DailyQuantity)
admin.site.register(DailyQuantityBad)
admin.site.register(DailyQuantityBySector)
admin.site.register(DailyQuantityBadBySector)
admin.site.register(PeopleQuantityBadLastFiveDays)
