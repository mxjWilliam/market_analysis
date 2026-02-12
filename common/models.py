from django.db import models


# 交易市场选项：A股、港股、美股等
MARKET_CHOICES = [
    ('CN', 'A股'),
    ('HK', '港股'),
    ('US', '美股'),
]


class TradingCalendar(models.Model):
    market = models.CharField(
        max_length=10,
        choices=MARKET_CHOICES,
        default='CN',
        verbose_name='交易市场',
        db_index=True,
    )
    date = models.DateField(verbose_name='交易日', db_index=True)
    open_time = models.TimeField(verbose_name='开盘时间')
    close_time = models.TimeField(verbose_name='收盘时间')
    is_trading_day = models.BooleanField(default=True, verbose_name='是否交易日')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '交易日历'
        verbose_name_plural = '交易日历'
        ordering = ['market', 'date']
        constraints = [
            models.UniqueConstraint(fields=['market', 'date'], name='unique_market_date'),
        ]

    def __str__(self):
        market_label = dict(MARKET_CHOICES).get(self.market, self.market)
        return f'{market_label} {self.date} ({"交易日" if self.is_trading_day else "非交易日"})'
