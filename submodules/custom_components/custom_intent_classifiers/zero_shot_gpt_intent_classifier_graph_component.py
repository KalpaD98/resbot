import logging
import os
from typing import Dict, Text, Any, List, Type, Tuple

from dotenv import load_dotenv
from joblib import dump, load
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
    DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, is_trainable=True
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

    @staticmethod
    def _get_training_data(training_data: TrainingData) -> Tuple[List[Text], List[Text]]:
        """Preprocess the training data. Retrieve the text messages and their corresponding intents."""
        print("Getting training data for ZeroShotGPTIntentClassifier")
        messages = [example.get(TEXT) for example in training_data.training_examples if example.get(TEXT)]
        print("messages: ", messages[:3])
        intents = [example.get(INTENT) for example in training_data.training_examples if example.get(INTENT)]
        print("intents: ", intents[:3])
        return messages, intents

    def train(self, training_data: TrainingData) -> Resource:

        print("Training ZeroShotGPTIntentClassifier")
        messages, intents = self._get_training_data(training_data)
        if len(messages) == 0:
            logger.debug(
                f"Cannot train '{self.__class__.__name__}'. No data was provided. "
                f"Skipping training of the classifier."
            )
        self.clf.fit(messages, intents)
        print("Trained ZeroShotGPTIntentClassifier")
        self.persist()
        return self._resource

    def persist(self) -> None:
        """Persist the intents into model storage."""
        print("Persisting ZeroShotGPTIntentClassifier")
        with self._model_storage.write_to(self._resource) as model_dir:
            dump(self.clf, model_dir / f"{self.name}.joblib")
            print("Persisted ZeroShotGPTIntentClassifier")
        # with self._model_storage.write_to(self._resource) as directory_path:
        #     json.dump(intents, open(directory_path / "gpt_intents.json", "w"))
        #     print("Persisted ZeroShotGPTIntentClassifier")

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
            # with model_storage.read_from(resource) as directory_path:
            #     intents = json.load(open(directory_path / "gpt_intents.json", "r"))
            #     component = cls(config, execution_context.node_name, model_storage, resource)
            #     component.clf.fit(None, intents)
            #     print("Loaded ZeroShotGPTIntentClassifier")
            #     return component
            with model_storage.read_from(resource) as model_dir:
                classifier = load(model_dir / f"{resource.name}.joblib")
                component = cls(
                    config, execution_context.node_name, model_storage, resource
                )
                component.clf = classifier
                print("Loaded ZeroShotGPTIntentClassifier")
                return component
        except ValueError:
            print("Failed to load: No data found for the given resource")
            # TODO: In this case can get data from training and add here
            return cls(config, execution_context.node_name, model_storage, resource)

    def process(self, messages: List[Message]) -> List[Message]:
        """Process the list of messages."""
        print("Processing ZeroShotGPTIntentClassifier")
        dummy_text = "dummy text"
        for message in messages:
            text = message.get(TEXT)
            if text:
                try:
                    # Adding dummy text to bypass the error
                    prediction = self.clf.predict([text, dummy_text])
                    print("prediction by gpt: ", prediction)
                    if prediction and prediction[0]:  # Checking if prediction[0] is not an empty string
                        # Set the intent of the message as the first prediction
                        # TODO: Add confidence score and uncomment the line below
                        # message.set(INTENT, {"name": prediction[0], "confidence": 0.5})
                        print("prediction of few shot: ", prediction[0])
                except Exception as e:
                    print(f"Failed to predict intent for text '{text}': {str(e)}")
        return messages
