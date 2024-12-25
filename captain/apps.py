from django.apps import AppConfig

class CaptainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'captain'

    def ready(self):
        import captain.signals  # استدعاء الإشارات
