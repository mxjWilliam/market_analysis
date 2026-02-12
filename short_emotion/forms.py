# -*- coding: utf-8 -*-
from django import forms
from .models import UpDonwNumber


class UpDonwNumberForm(forms.ModelForm):
    """手动插入 UpDonwNumber 的表单"""

    class Meta:
        model = UpDonwNumber
        fields = [
            'trading_date',
            'up_number',
            'down_number',
            'up_floor_number',
            'up_floor_number2',
            'down_floor_number',
            'floor_explosion_number',
            'up_twenty_number',
            'up_thirty_number',
            'up_fourty_number',
            'up_gt_fourty_number',
        ]
        widgets = {
            'trading_date': forms.DateInput(attrs={'type': 'date'}),
            'up_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'down_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'up_floor_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'up_floor_number2': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'down_floor_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'floor_explosion_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'up_twenty_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'up_thirty_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'up_fourty_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
            'up_gt_fourty_number': forms.NumberInput(attrs={'min': 0, 'class': 'form-num'}),
        }
        labels = {
            'trading_date': '交易日期',
            'up_number': '上涨家数',
            'down_number': '下跌家数',
            'up_floor_number': '涨停家数',
            'up_floor_number2': '非一字涨停家数',
            'down_floor_number': '跌停家数',
            'floor_explosion_number': '炸板家数',
            'up_twenty_number': '二连板',
            'up_thirty_number': '三连板',
            'up_fourty_number': '四连板',
            'up_gt_fourty_number': '四连板以上',
        }
