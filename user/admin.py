from django.contrib import admin
from .models import UserProfile, UserProfileFile, UserPassword

admin.site.register(UserProfile)
admin.site.register(UserProfileFile)
admin.site.register(UserPassword)
