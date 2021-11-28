from django.contrib import admin
from .models import UserProfile, UserProfileFile, UserPassword


class UserPasswordAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'get_user_name', 'password')

    @admin.display(ordering='user_id__name', description='Nome')
    def get_user_name(self, obj):
        return obj.user_id.first_name


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'name', 'birth_date', 'user_type', 'sector_id')


class UserProfileFileAdmin(admin.ModelAdmin):
    list_display = ('import_file', 'create_at')


admin.site.register(UserPassword, UserPasswordAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserProfileFile, UserProfileFileAdmin)
