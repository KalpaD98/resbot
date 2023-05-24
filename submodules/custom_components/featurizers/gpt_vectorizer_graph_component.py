from typing import Dict, Text, Any, List, Type

from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.constants import TEXT
from rasa.shared.nlu.training_data.message import Message
from skllm.preprocessing import GPTVectorizer


@DefaultV1Recipe.register(
    [DefaultV1Recipe.ComponentType.MESSAGE_FEATURIZER], is_trainable=False
)
class GPTVectorizerComponent(GraphComponent):
    @classmethod
    def required_components(cls) -> List[Type]:
        """Components that should be included in the pipeline before this component."""
        return []

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> GraphComponent:
        gpt_model = GPTVectorizer()  # initialize GPT Vectorizer
        return cls(model_storage, resource, gpt_model)

    def __init__(self, model_storage: ModelStorage, resource: Resource, gpt_model: GPTVectorizer):
        self._model_storage = model_storage
        self._resource = resource
        self._gpt_model = gpt_model

    def process(self, messages: List[Message]) -> List[Message]:
        for message in messages:
            # transform the message text into an embedding vector
            vector = self._gpt_model.transform([message.get(TEXT)])
            message.set('text_embedding', vector)
        return messages
