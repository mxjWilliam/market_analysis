# Generated manually for TradingCalendar market field and PK change

from django.db import migrations, models


def migrate_trading_calendar(apps, schema_editor):
    """将旧表数据迁移到新表结构，SQLite 需要重建表以实现主键变更"""
    from django.db import connection

    with schema_editor.connection.cursor() as cursor:
        if connection.vendor == 'sqlite':
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS common_tradingcalendar_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    market VARCHAR(10) NOT NULL DEFAULT 'CN',
                    date DATE NOT NULL,
                    open_time TIME NOT NULL,
                    close_time TIME NOT NULL,
                    is_trading_day BOOLEAN NOT NULL DEFAULT 1,
                    created_at DATETIME NOT NULL,
                    updated_at DATETIME NOT NULL
                )
            """)
            cursor.execute("""
                INSERT INTO common_tradingcalendar_new
                (id, market, date, open_time, close_time, is_trading_day, created_at, updated_at)
                SELECT rowid, 'CN', date, open_time, close_time, is_trading_day, created_at, updated_at
                FROM common_tradingcalendar
            """)
            cursor.execute("DROP TABLE common_tradingcalendar")
            cursor.execute("ALTER TABLE common_tradingcalendar_new RENAME TO common_tradingcalendar")
            cursor.execute("""
                CREATE UNIQUE INDEX common_tradingcalendar_market_date_uniq
                ON common_tradingcalendar (market, date)
            """)
        elif connection.vendor == 'mysql':
            # MySQL: 新建表、复制数据、替换
            cursor.execute("""
                CREATE TABLE common_tradingcalendar_new (
                    id BIGINT AUTO_INCREMENT PRIMARY KEY,
                    market VARCHAR(10) NOT NULL DEFAULT 'CN',
                    date DATE NOT NULL,
                    open_time TIME(6) NOT NULL,
                    close_time TIME(6) NOT NULL,
                    is_trading_day TINYINT(1) NOT NULL DEFAULT 1,
                    created_at DATETIME(6) NOT NULL,
                    updated_at DATETIME(6) NOT NULL,
                    UNIQUE KEY unique_market_date (market, date)
                )
            """)
            cursor.execute("""
                INSERT INTO common_tradingcalendar_new
                (market, date, open_time, close_time, is_trading_day, created_at, updated_at)
                SELECT 'CN', date, open_time, close_time, is_trading_day, created_at, updated_at
                FROM common_tradingcalendar
            """)
            cursor.execute("DROP TABLE common_tradingcalendar")
            cursor.execute("RENAME TABLE common_tradingcalendar_new TO common_tradingcalendar")
        elif connection.vendor == 'postgresql':
            cursor.execute(
                "ALTER TABLE common_tradingcalendar ADD COLUMN market VARCHAR(10) NOT NULL DEFAULT 'CN'"
            )
            cursor.execute("ALTER TABLE common_tradingcalendar ADD COLUMN id SERIAL")
            cursor.execute(
                "UPDATE common_tradingcalendar SET id = nextval('common_tradingcalendar_id_seq')"
            )
            cursor.execute("ALTER TABLE common_tradingcalendar ALTER COLUMN id SET NOT NULL")
            cursor.execute("ALTER TABLE common_tradingcalendar DROP CONSTRAINT common_tradingcalendar_pkey")
            cursor.execute("ALTER TABLE common_tradingcalendar ADD PRIMARY KEY (id)")
            cursor.execute(
                "CREATE UNIQUE INDEX common_tradingcalendar_market_date_uniq "
                "ON common_tradingcalendar (market, date)"
            )
        else:
            raise NotImplementedError(
                f"主键迁移暂不支持 {connection.vendor}，"
                "请在 PostgreSQL、MySQL 或 SQLite 下运行"
            )


def reverse_migrate(apps, schema_editor):
    """回滚：恢复旧表结构（生产环境谨慎使用）"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='tradingcalendar',
                    name='date',
                    field=models.DateField(db_index=True, verbose_name='交易日'),
                ),
                migrations.AddField(
                    model_name='tradingcalendar',
                    name='id',
                    field=models.BigAutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name='ID'
                    ),
                ),
                migrations.AddField(
                    model_name='tradingcalendar',
                    name='market',
                    field=models.CharField(
                        choices=[('CN', 'A股'), ('HK', '港股'), ('US', '美股')],
                        db_index=True,
                        default='CN',
                        max_length=10,
                        verbose_name='交易市场',
                    ),
                ),
                migrations.AddConstraint(
                    model_name='tradingcalendar',
                    constraint=models.UniqueConstraint(
                        fields=('market', 'date'),
                        name='unique_market_date',
                    ),
                ),
            ],
            database_operations=[
                migrations.RunPython(migrate_trading_calendar, reverse_migrate),
            ],
        ),
    ]
