from typing import Any, Text, Dict, List

from googletrans import Translator
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

from actions.all_actions.helper_functions.response_generator.constants import SIN
from submodules.custom_components.language_detection.language_detector import LanguageDetector


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR, DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER],
    is_trainable=False
)
class LanguageHandler(GraphComponent):
    """A new GraphComponent for language handling."""

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
            "project_id": 'still-resource-318401',
            "location": "global"
        }

    def __init__(
            self,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext
    ) -> None:
        self._config = config
        self._execution_context = execution_context
        self._model_storage = model_storage
        self._resource = resource

    def process(self, messages: List[Message]) -> List[Message]:
        translator = Translator()
        print("---------------------LanguageHandler---------------------")
        for message in messages:
            print(message.get('text'))
            text = message.get('text')

            # Detect languages
            detected_languages = LanguageDetector.detect_languages(text)

            # Set the language slot based on the detected languages
            language = 'en'  # Default to English
            probability = 1

            for lang, prob in detected_languages:
                if lang == SIN:
                    language = SIN
                    probability = prob
                    # Translate the text to English
                    translated_text = translator.translate(text, src='si', dest='en')
                    text = translated_text.text  # Update the text with the translated version
                    break

            # Set the language entity
            entity = {
                'value': language,
                'confidence': probability,
                'entity': 'language',
                'extractor': 'LanguageHandler'
            }
            message.set("entities", [entity], add_to_output=True)

            # Update the message's text with the translated version
            message.set('text', text.lower(), add_to_output=True)
            print(message.get('text'), message.get('entities'))

        print("---------------------LanguageHandler Ended---------------------")
        return messages

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        """Process the training data in-place."""
        return training_data

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext
    ) -> 'LanguageHandler':
        return cls(config, model_storage, resource, execution_context)

    def persist(self) -> None:
        """Persist this component to disk for future loading."""
        pass

    @classmethod
    def load(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> 'LanguageHandler':
        return cls(config, model_storage, resource, execution_context)
