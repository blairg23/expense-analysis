from django.contrib import admin

from expensive.models import ExtendedUser, UserType, Transaction


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'slug']
    list_display_links = list_display


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_date', 'post_date', 'amount', 'description', 'category', 'type', 'source', 'owner']
    list_display_links = list_display

    def category(self, instance):
        return ", ".join([str(category) for category in instance.category.all()])
