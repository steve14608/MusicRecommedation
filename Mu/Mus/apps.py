from django.apps import AppConfig
import pickle

MUSIC_MODEL = None
SINGER_MODEL = None


class MusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Mus'

    def ready(self):
        """
        项目启动时加载模型到内存。
        """
        global MUSIC_MODEL
        global SINGER_MODEL
        with open("F:/itemcf_model.pkl", "rb") as f:
            MUSIC_MODEL = pickle.load(f)
        with open("F:/itemcf_singerid_model.pkl", 'rb') as f:
            SINGER_MODEL = pickle.load(f)
        print("Model loaded successfully!")
