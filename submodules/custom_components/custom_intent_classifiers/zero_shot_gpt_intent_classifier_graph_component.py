import json
import os
from typing import Dict, Text, Any, List, Optional

from dotenv import load_dotenv
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.constants import INTENT
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from skllm.config import SKLLMConfig
from skllm.models.gpt_zero_shot_clf import ZeroShotGPTClassifier

load_dotenv()


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, is_trainable=True
)
class ZeroShotGPTIntentClassifier(GraphComponent):
    def __init__(self, model_storage: ModelStorage, resource: Resource, training_artifact: Optional[Dict] = None,
                 ) -> None:
        print("init ZeroShotGPTIntentClassifier")
        self._model_storage = model_storage
        self._resource = resource
        self.clf = ZeroShotGPTClassifier()  # initialize the classifier here

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
        return cls(model_storage, resource)

    @classmethod
    def load(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
            **kwargs: Any,
    ) -> GraphComponent:
        # Load persisted classifier
        try:
            with model_storage.read_from(resource) as directory_path:
                with open(directory_path / "intents.json", "r") as file:
                    intents = json.load(file)
                    print("json.load(file) ZeroShotGPTIntentClassifier")
                    return cls(model_storage, resource, intents)

        except ValueError:
            # No persisted data found for the given resource
            return cls(model_storage, resource)

    def train(self, training_data: TrainingData) -> Resource:
        print("Training ZeroShotGPTIntentClassifier")
        # Extract intents from training data
        intents = list(set([example.get(INTENT) for example in training_data.training_examples]))

        # Fit ZeroShotGPTClassifier
        self.clf.fit(None, intents)

        # Persist the classifier
        with self._model_storage.write_to(self._resource) as directory_path:
            with open(directory_path / "intents.json", "w") as file:
                json.dump(intents, file)
        print("Training ZeroShotGPTIntentClassifier complete")
        return self._resource

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            print("Start processing using ZeroShotGPTIntentClassifier")
            if message.data.get(INTENT) is None:
                # Only classify intent if it's not available yet in the message
                intents = self.clf.predict([message.get("text")])
                print("intents: ", intents if intents is not None else "None")
                message.data[INTENT] = {
                    "name": intents[0],
                    "confidence": 0.6,
                    # you might need to handle confidence in a different way
                }
            else:
                print("INTENT already exists in message")
                print(message.get("text") if message.get("text") is not None else "no message")
                # intents = self.clf.predict([message.get("text")])
                print("Predicted intents by ZeroShotGPTIntentClassifier: ")
                # print("intents: ", intents if intents is not None else "None")
            print("Processing using ZeroShotGPTIntentClassifier ended")
        return messages
