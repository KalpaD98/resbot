import json
import os
from typing import Dict, Text, Any, List, Tuple, Type

from dotenv import load_dotenv
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.classifiers.classifier import IntentClassifier
from rasa.shared.nlu.constants import INTENT, TEXT
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from skllm import ZeroShotGPTClassifier
from skllm.config import SKLLMConfig

load_dotenv()


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, is_trainable=True
)
class ZeroShotGPTIntentClassifier(IntentClassifier, GraphComponent):
    @classmethod
    def required_components(cls) -> List[Type]:
        return []

    @classmethod
    def required_packages(cls) -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return ["skllm"]

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {}

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validates that the component is configured properly."""
        pass

    def __init__(self, config: Dict[Text, Any], name: Text, model_storage: ModelStorage, resource: Resource) -> None:
        print("init ZeroShotGPTIntentClassifier")
        self._model_storage = model_storage
        self._resource = resource
        self.name = name
        self.clf = ZeroShotGPTClassifier()

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> GraphComponent:

        # Fetch the OpenAI key and organization from environment variables
        openai_key = os.getenv("OPENAI_KEY")
        openai_organization = os.getenv("OPENAI_ORGANIZATION")

        # Set the OpenAI key and organization for SKLLMConfig
        SKLLMConfig.set_openai_key(openai_key)
        SKLLMConfig.set_openai_org(openai_organization)
        print("create ZeroShotGPTIntentClassifier")
        return cls(config, execution_context.node_name, model_storage, resource)

    @classmethod
    def load(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
            **kwargs: Any,
    ) -> GraphComponent:
        print("Loading ZeroShotGPTIntentClassifier")
        try:
            with model_storage.read_from(resource) as directory_path:
                intents = json.load(open(directory_path / "gpt_intents.json", "r"))
                component = cls(config, execution_context.node_name, model_storage, resource)
                component.clf.fit(None, intents)
                print("Loaded ZeroShotGPTIntentClassifier")
                return component
        except ValueError:
            print("No data found for the given resource")
            return cls(config, execution_context.node_name, model_storage, resource)

    def _get_training_data(self, training_data: TrainingData) -> Tuple[List[Text], List[Text]]:
        """Retrieve the text messages and their corresponding intents."""
        print("Getting training data for ZeroShotGPTIntentClassifier")
        messages = [example.get(TEXT) for example in training_data.training_examples if example.get(TEXT)]
        print("messages: ", messages)
        intents = [example.get(INTENT) for example in training_data.training_examples if example.get(INTENT)]
        print("intents: ", intents)
        return messages, intents

    def process_training_data(self, training_data: TrainingData) -> None:
        """Preprocess the training data."""
        print("Processing training data for ZeroShotGPTIntentClassifier")
        messages, intents = self._get_training_data(training_data)
        self.clf.fit(messages, intents)

    def process(self, messages: List[Message]) -> List[Message]:
        """Process the list of messages."""
        print("Processing ZeroShotGPTIntentClassifier")
        for message in messages:
            text = message.get(TEXT)
            if text:
                prediction = self.clf.predict([text])
                if prediction:
                    message.set(INTENT, {"name": prediction[0], "confidence": 1.0})

        return messages

    def persist(self) -> None:
        print("Persisting ZeroShotGPTIntentClassifier")
        intents = self.clf.classes_.tolist()
        with self._model_storage.write_to(self._resource) as directory_path:
            json.dump(intents, open(directory_path / "gpt_intents.json", "w"))
