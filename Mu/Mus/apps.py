from django.apps import AppConfig
import pickle
from . import model_manager


class MusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Mus'

    def ready(self):
        """
        项目启动时加载模型到内存。
        """
        model_manager.model_manager.load_models("F:/song.pkl", "F:/singer.pkl")
        print("Model loaded successfully!")
