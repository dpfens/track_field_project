from django.apps import AppConfig


class IdentityConfig(AppConfig):
    name = 'identity'
    verbose_name = 'Identity Management'

    def ready(self):
        import from identity import signals
