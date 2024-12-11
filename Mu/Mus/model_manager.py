# model_manager.py
import pickle


class ModelManager:
    def __init__(self):
        self.MUSIC_MODEL = None
        self.SINGER_MODEL = None

    def load_models(self, music_model_path, singer_model_path):
        # self.MUSIC_MODEL = load_similarity_dict(music_model_path)
        # self.SINGER_MODEL = load_similarity_dict(singer_model_path)
        with open(music_model_path, 'rb') as f:
            self.MUSIC_MODEL = pickle.load(f)
        with open(singer_model_path, 'rb') as f:
            self.SINGER_MODEL = pickle.load(f)


model_manager = ModelManager()
