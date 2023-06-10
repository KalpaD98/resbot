from typing import Any, Text, Dict, List

from googletrans import Translator
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData

from actions.all_actions.helper_functions.response_generator.constants import SIN
from submodules.custom_components.language_handlers.language_detector import LanguageDetector


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.ENTITY_EXTRACTOR, DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER],
    is_trainable=False
)
class LanguageHandlerAndTranslator(GraphComponent):
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

            text = ' '.join(message.get('text').splitlines())
            print(text)

            # Detect languages
            detected_languages = LanguageDetector.detect_languages(text)

            # Set the language slot based on the detected languages
            language = 'en'  # Default to English
            probability = 1

            for lang, prob in detected_languages:
                if lang == SIN:

                    # Translate the text to English
                    translated_text = translator.translate(text, src='si', dest='en')
                    text = translated_text.text  # Update the text with the translated version
                    print("translated message: " + text)
                    message.set('text', text, add_to_output=True)
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
    ) -> 'LanguageHandlerAndTranslator':
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
    ) -> 'LanguageHandlerAndTranslator':
        return cls(config, model_storage, resource, execution_context)
