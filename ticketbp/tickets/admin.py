from django.contrib import admin

from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'extra_fee_rate', 'display_priority')
    ordering = ('-display_priority', 'name')


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('name', 'category', 'status', 'start_date')
    list_select_related = ('category',)
    ordering = ('-created_at',)
