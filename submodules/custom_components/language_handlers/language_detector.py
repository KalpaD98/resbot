import warnings
from typing import List, Tuple

import fasttext


class LanguageDetector:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        # load language identification model
        model = fasttext.load_model("submodules/custom_components/language_handlers/models/lid.176.bin")

    @staticmethod
    def detect_languages(text: str, k: int = 2) -> List[Tuple[str, float]]:
        labels, probs = LanguageDetector.model.predict(text, k=k)
        detected_languages = [(label[-2:], prob) for label, prob in zip(labels, probs)]
        return detected_languages

