from django.apps import AppConfig

from .model_manager import model_manager

class MusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Mus'

    def ready(self):
        model_manager.load_models(
            "F:/sing.pkl",
            "F:/singer.pkl"
        )
        print("Models loaded successfully!")

