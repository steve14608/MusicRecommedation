# model_manager.py
import pickle


def load_similarity_dict(file_path):
    with open(file_path, 'rb') as file:
        recommendations = pickle.load(file)
    return recommendations


class ModelManager:
    def __init__(self):
        self.MUSIC_MODEL = None
        self.SINGER_MODEL = None

    def load_models(self, music_model_path, singer_model_path):
        self.MUSIC_MODEL = load_similarity_dict(music_model_path)
        self.SINGER_MODEL = load_similarity_dict(singer_model_path)


model_manager = ModelManager()
