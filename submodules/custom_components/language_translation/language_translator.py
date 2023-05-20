from typing import Any, Text, Dict, List

from google.cloud import translate
from rasa.engine.graph import ExecutionContext, GraphComponent
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message

from submodules.custom_components.language_detection.language_detector import LanguageDetector


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
        self._client = translate.TranslationServiceClient()
        self._parent = f"projects/{self._config['project_id']}/locations/{self._config['location']}"

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            text = message.get('text')

            # language detection request
            detected_languages = self._client.detect_language(
                request={
                    "parent": self._parent,
                    "content": text,
                    "mime_type": "text/plain",
                }
            )

            detected_language = detected_languages.languages[0]

            # translating to french when necessary
            if detected_language.language_code == 'si':
                response = self._client.translate_text(
                    request={
                        "parent": self._parent,
                        "contents": [text],
                        "mime_type": "text/plain",
                        "source_language_code": "si",
                        "target_language_code": "en-US",
                    }
                )

                # changing the input message's text after translation
                message.set('text', response.translations[0].translated_text)

            # modified to add language entity

            detected_languages = LanguageDetector.detect_languages(text)

            # Set the language slot based on the detected languages
            language = 'en'  # Default to English
            probability = 0
            for lang, prob in detected_languages:
                if lang == 'si':
                    language = 'si'
                    probability = prob
                    break

            # modification end

            # setting a language entity, so it can be used by custom actions

            entity = {
                'value': language,
                'confidence': probability,
                'entity': 'language',
                'extractor': 'LanguageHandler'
            }

            message.set("entities", [entity], add_to_output=True)
        return messages

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

# modified below from line 63 onwards
#
# # setting a language entity, so it can be used by custom actions
#
# entity = {
#     'value': detected_language.language_code,
#     'confidence': detected_language.confidence,
#     'entity': 'language',
#     'extractor': 'LanguageHandler'
# }