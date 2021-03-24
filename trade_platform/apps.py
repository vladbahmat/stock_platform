from django.apps import AppConfig


class TradePlatformConfig(AppConfig):
    name = 'trade_platform'

    def ready(self):
        import trade_platform.signals
