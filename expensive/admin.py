from django.contrib import admin

from expensive.models import ExtendedUser, UserType, TransactionType, Transaction, Category, Source


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(ExtendedUser)
class ExtendedUserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'slug']
    list_display_links = list_display


@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ['transaction_type']
    list_display_links = list_display


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    list_display = ['source']
    list_display_links = list_display


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'description']
    list_display_links = list_display


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['transaction_date', 'post_date', 'amount', 'description', 'categories', 'accounting_type', 'semantic_type', 'source', 'owner']
    list_display_links = ['transaction_date', 'post_date', 'amount', 'description', 'accounting_type', 'semantic_type', 'source', 'owner']
    list_filter = ['source', 'category']

    list_select_related = ['type', 'source', 'owner']

    def categories(self, transaction):
        return ", ".join([str(category) for category in transaction.category.all()])
