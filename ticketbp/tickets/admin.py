from django.contrib import admin

from . import models

#inlineの追加
class AnswerInline(admin.StackedInline):
	model = models.Answer

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


@admin.register(models.AnswerReview)
class AnswerReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(models.OnayamiTicket)
class OnayamiTicketAdmin(admin.ModelAdmin):
    list_filter = ('solved_status',)
    list_display = ('name', 'category', 'solved_status')
    list_select_related = ('category',)
    ordering = ('-created_at',)
    inlines = [AnswerInline]