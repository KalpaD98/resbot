import os
from typing import Dict, Text, Any, List, Type

from rasa.engine.graph import GraphComponent
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.constants import FEATURIZER_CLASS_ALIAS
from rasa.nlu.featurizers.dense_featurizer.dense_featurizer import DenseFeaturizer
from rasa.nlu.tokenizers.tokenizer import Tokenizer
from rasa.shared.nlu.constants import TEXT, FEATURE_TYPE_SENTENCE
from rasa.shared.nlu.training_data.features import Features
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from skllm.config import SKLLMConfig
from skllm.preprocessing import GPTVectorizer


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER], is_trainable=False
)
class GPTVectorFeaturizer(DenseFeaturizer, GraphComponent):
    @classmethod
    def required_components(cls) -> List[Type]:
        """Components that should be included in the pipeline before this component."""
        return [Tokenizer]

    @staticmethod
    def required_packages() -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return []

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            name: Text,
            model_storage: ModelStorage,
            resource: Resource,
    ) -> GraphComponent:

        return cls(name, config)

    def __init__(self, name: Text, config: Dict[Text, Any]):
        super().__init__(name=name, config=config)
        openai_key = os.getenv("OPENAI_KEY")
        openai_organization = os.getenv("OPENAI_ORGANIZATION")

        # Set the OpenAI key and organization for SKLLMConfig
        SKLLMConfig.set_openai_key(openai_key)
        SKLLMConfig.set_openai_org(openai_organization)

        self._gpt_model = GPTVectorizer()

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            self._set_features(message, TEXT)

        return messages

    def process_training_data(self, training_data: TrainingData) -> TrainingData:
        for example in training_data.training_examples:
            self._set_features(example, TEXT)

        return training_data

    def _set_features(self, message: Message, attribute: Text = TEXT) -> None:
        text = message.get(attribute)

        if text:
            # vector = self._gpt_model.transform([text]).reshape(1, -1)
            vector = self._gpt_model.transform_single(text).reshape(1, -1)
            final_features = Features(
                vector,
                FEATURE_TYPE_SENTENCE,
                attribute,
                self._config[FEATURIZER_CLASS_ALIAS],
            )
            print(final_features)
            # TODO: uncomment below
            # message.add_features(final_features)

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validates that the component is configured properly."""
        pass
