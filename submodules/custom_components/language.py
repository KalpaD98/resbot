from typing import List, Tuple

import fasttext

model = fasttext.load_model("lid.176.bin")


# !wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

def detect_languages(text: str, k: int = 2) -> List[Tuple[str, float]]:
    labels, probs = model.predict(text, k=k)
    detected_languages = [(label[-2:], prob) for label, prob in zip(labels, probs)]
    return detected_languages


# Test with example messages
english_msg = "Hello, how are you?"
sinhala_msg = "ඔයාගේ නම මොනවාද?"
mixed_msg = "මට අවිස්සාවේ : How can I help you?"

print("English message:", detect_languages(english_msg))
print("Sinhala message:", detect_languages(sinhala_msg))
print("Mixed message:", detect_languages(mixed_msg))
