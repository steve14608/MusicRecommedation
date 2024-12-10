from django.apps import AppConfig
from .model_manager import model_manager
class MusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Mus'

    def ready(self):
        model_manager.load_models(
            "F:/itemcf_model.pkl",
            "F:/itemcf_singerid_model.pkl"
        )
        print("Models loaded successfully!")