from django.contrib import admin

from expensive.models import ExtendedUser, UserType

@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'slug']
    list_display_links = list_display