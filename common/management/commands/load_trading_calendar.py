from django.core.management.base import BaseCommand
from common.utils import load_trading_calendar_for_year


class Command(BaseCommand):
    help = (
        '根据 akshare 交易日历加载指定年份数据到 TradingCalendar，例如: '
        'load_trading_calendar 2026 [--market CN]'
    )

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='年份，如 2026')
        parser.add_argument(
            '--market',
            type=str,
            default='CN',
            choices=['CN', 'HK', 'US'],
            help='交易市场，CN=A股/HK=港股/US=美股，默认 CN（当前 akshare 仅支持 A 股）',
        )

    def handle(self, *args, **options):
        year = options['year']
        market = options['market']
        try:
            total, trading = load_trading_calendar_for_year(year, market=market)
            self.stdout.write(
                self.style.SUCCESS(
                    f'已加载 {market} {year} 年交易日历: 共 {total} 条，其中交易日 {trading} 条'
                )
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'加载失败: {e}'))
            raise
