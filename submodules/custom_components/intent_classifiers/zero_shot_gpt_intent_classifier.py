import logging
import os
from typing import Dict, Text, Any, List, Type, Optional

from dotenv import load_dotenv
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.constants import INTENT, TEXT
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from skllm import ZeroShotGPTClassifier
from skllm.config import SKLLMConfig

load_dotenv()
logger = logging.getLogger(__name__)


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, is_trainable=False
)
class ZeroShotGPTIntentClassifier(GraphComponent):
    @classmethod
    def required_components(cls) -> List[Type]:
        return []

    @classmethod
    def required_packages(cls) -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return []

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {}

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validates that the component is configured properly."""
        pass

    def __init__(self, config: Dict[Text, Any], name: Text, model_storage: ModelStorage, resource: Resource) -> None:
        print("init ZeroShotGPTIntentClassifier")
        self.name = name

        # Fetch the OpenAI key and organization from environment variables
        openai_key = os.getenv("OPENAI_KEY")
        openai_organization = os.getenv("OPENAI_ORGANIZATION")

        # Set the OpenAI key and organization for SKLLMConfig
        SKLLMConfig.set_openai_key(openai_key)
        SKLLMConfig.set_openai_org(openai_organization)

        self.clf = ZeroShotGPTClassifier()

        self._model_storage = model_storage
        self._resource = resource

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> GraphComponent:

        return cls(config, execution_context.node_name, model_storage, resource)

    @classmethod
    def load(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
            training_data: Optional[TrainingData] = None,
            **kwargs: Any,
    ) -> GraphComponent:

        print("Loading ZeroShotGPTIntentClassifier")
        openai_key = os.getenv("OPENAI_KEY")
        openai_organization = os.getenv("OPENAI_ORGANIZATION")

        # Set the OpenAI key and organization for SKLLMConfig
        SKLLMConfig.set_openai_key(openai_key)
        SKLLMConfig.set_openai_org(openai_organization)
        try:

            print("Loaded ZeroShotGPTIntentClassifier")
            # training
            if training_data:
                print("Training ZeroShotGPTIntentClassifier")
                intents = cls._get_training_data(training_data)
                cls.clf.fit(None, intents)
                print("Trained ZeroShotGPTIntentClassifier")
                # training complete
            return cls.clf
        except ValueError:
            print("Failed to load: No data found for the given resource")
            return cls(config, execution_context.node_name, model_storage, resource)

    def process(self, messages: List[Message]) -> List[Message]:
        """Process the list of messages."""
        # TODO: predict only if DIET fails
        print("Processing ZeroShotGPTIntentClassifier")
        for message in messages:
            text = message.get(TEXT)
            if text:
                try:
                    # Adding dummy text to bypass the error
                    prediction = self.clf.predict_single(text)
                    print("prediction by gpt: ", prediction)
                    if prediction:
                        # Set the intent of the message as the first prediction
                        # TODO: Add confidence score and uncomment the line below
                        # We can get DIET predictions here
                        # message.set(INTENT, {"name": prediction[0], "confidence": 0.5})
                        # Create a methodology to solve this issue
                        print("prediction of zero shot: ", prediction[0])
                except Exception as e:
                    print(f"Failed to predict intent for text '{text}': {str(e)}")
        return messages

    @staticmethod
    def _get_training_data(training_data: TrainingData) -> set[Any]:
        """Preprocess the training data. Retrieve the text messages and their corresponding intents."""
        print("Getting training data for ZeroShotGPTIntentClassifier")

        unique_intents = set()

        for example in training_data.training_examples:
            intent = example.get(INTENT)

            if intent and intent not in unique_intents:
                unique_intents.add(intent)
        return unique_intents
