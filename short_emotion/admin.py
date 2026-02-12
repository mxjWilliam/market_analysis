from django import forms
from django.contrib import admin
from .models import UpDonwNumber


@admin.register(UpDonwNumber)
class UpDonwNumberAdmin(admin.ModelAdmin):
    list_display = (
        'trading_date', 'up_number', 'down_number',
        'up_floor_number', 'up_floor_number2', 'down_floor_number',
        'floor_explosion_number', 'up_twenty_number', 'up_thirty_number',
        'up_fourty_number', 'up_gt_fourty_number', 'update_time'
    )
    list_editable = (
        'up_number', 'down_number', 'up_floor_number', 'up_floor_number2',
        'down_floor_number', 'floor_explosion_number',
        'up_twenty_number', 'up_thirty_number', 'up_fourty_number', 'up_gt_fourty_number'
    )
    ordering = ('-trading_date',)
    list_per_page = 20
    search_fields = ()
    date_hierarchy = 'trading_date'

    fieldsets = (
        ('基础', {
            'fields': ('trading_date', 'up_number', 'down_number'),
            'description': '交易日期、上涨家数、下跌家数',
        }),
        ('涨跌停与炸板', {
            'fields': ('up_floor_number', 'up_floor_number2', 'down_floor_number', 'floor_explosion_number'),
        }),
        ('连板', {
            'fields': ('up_twenty_number', 'up_thirty_number', 'up_fourty_number', 'up_gt_fourty_number'),
        }),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'trading_date':
            kwargs['widget'] = forms.DateInput(attrs={'type': 'date'})
            kwargs['input_formats'] = ['%Y-%m-%d']
        return super().formfield_for_dbfield(db_field, request, **kwargs)
