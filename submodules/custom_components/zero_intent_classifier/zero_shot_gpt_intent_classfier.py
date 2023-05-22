from typing import Dict, Text, Any, List

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from rasa.shared.nlu.constants import INTENT
from skllm import ZeroShotGPTClassifier
from skllm.config import SKLLMConfig


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, is_trainable=True
)
class ZeroShotGPTIntentClassifier(GraphComponent):

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> GraphComponent:
        # Initialize ZeroShotGPTClassifier
        SKLLMConfig.set_openai_key("<YOUR_KEY>")
        SKLLMConfig.set_openai_org("<YOUR_ORGANISATION>")

        return cls(resource)

    def __init__(self, resource: Resource) -> None:
        self._resource = resource

    def train(self, training_data: TrainingData) -> Resource:
        # Extract intents from training data
        intents = list(set([example.get(INTENT) for example in training_data.intent_examples]))

        # Initialize and fit ZeroShotGPTClassifier
        self.clf = ZeroShotGPTClassifier(openai_model="gpt-3.5-turbo")
        self.clf.fit(None, intents)

        return self._resource

    def process(self, messages: List[Message]) -> List[Message]:
        # Process each message
        for message in messages:
            # Predict the intent
            predicted_intent = self.clf.predict([message.text])[0]

            # Update the message with the predicted intent
            message.set(INTENT, predicted_intent, add_to_output=True)

        return messages
