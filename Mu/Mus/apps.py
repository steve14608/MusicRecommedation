from django.apps import AppConfig
import pickle

MODEL = None


class MusConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Mus'

    def ready(self):
        """
        项目启动时加载模型到内存。
        """
        global MODEL
        model_path = "F:/itemcf_model.pkl"
        with open(model_path, "rb") as f:
            MODEL = pickle.load(f)
        print("Model loaded successfully!")
