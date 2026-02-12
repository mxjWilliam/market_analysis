from django.contrib import admin
from .models import TradingCalendar


@admin.register(TradingCalendar)
class TradingCalendarAdmin(admin.ModelAdmin):
    list_display = ('date', 'open_time', 'close_time', 'is_trading_day', 'created_at', 'updated_at')
    list_editable = ('open_time', 'close_time', 'is_trading_day')
    list_filter = ('is_trading_day',)
    search_fields = ('date',)
    ordering = ('-date',)
    list_per_page = 20
    date_hierarchy = 'date'

    fieldsets = (
        ('日期与类型', {
            'fields': ('date', 'is_trading_day'),
            'description': '交易日、是否交易日',
        }),
        ('交易时间', {
            'fields': ('open_time', 'close_time'),
        }),
    )
