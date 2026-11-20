from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("title", "owner", "amount", "category", "spent_on")
    list_filter = ("category", "spent_on")
    search_fields = ("title", "owner__username")
