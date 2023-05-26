import logging
from typing import Dict, Text, Any, List, Type

from dotenv import load_dotenv
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.shared.nlu.constants import INTENT, TEXT, INTENT_RANKING_KEY
from rasa.shared.nlu.training_data.message import Message
from rasa.shared.nlu.training_data.training_data import TrainingData
from transformers import pipeline

load_dotenv()
logger = logging.getLogger(__name__)


@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.INTENT_CLASSIFIER, is_trainable=False
)
class ZeroShotBartIntentClassifier(GraphComponent):
    @classmethod
    def required_components(cls) -> List[Type]:
        return []

    @classmethod
    def required_packages(cls) -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return []

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {"candidate_class_size": 5}

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validates that the component is configured properly."""
        pass

    def __init__(self, config: Dict[Text, Any], name: Text, model_storage: ModelStorage, resource: Resource) -> None:
        print("init ZeroShotBartIntentClassifier")
        self.name = name
        self.clf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self._model_storage = model_storage
        self._resource = resource
        self.candidate_class_size = config["candidate_class_size"]

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> GraphComponent:
        return cls(config, execution_context.node_name, model_storage, resource)

    # @classmethod
    # def load(
    #         cls,
    #         config: Dict[Text, Any],
    #         model_storage: ModelStorage,
    #         resource: Resource,
    #         execution_context: ExecutionContext,
    #         training_data: Optional[TrainingData] = None,
    #         **kwargs: Any,
    # ) -> GraphComponent:
    #
    #     return cls(config, execution_context.node_name, model_storage, resource)

    def process(self, messages: List[Message]) -> List[Message]:
        """Process the list of messages."""
        # TODO: predict only if DIET fails
        # check if nlu_fallback
        print("Processing ZeroShotBartIntentClassifier")
        for message in messages:
            intent_ranking = message.get(INTENT_RANKING_KEY)
            intent = message.get(INTENT)
            print("Process ZERO SHOT Bart Classifier")
            print()
            print(intent_ranking)
            print("intent: ", intent)
            print()
            print("Process ZERO SHOT Bart Classifier complete")
            text = message.get(TEXT)
            if text:  # check for intent being nlu_fallback if yes then run below code
                try:
                    # get from DIET and add from GPT pretrain and add other
                    candidate_labels = self.get_candidate_labels(intent_ranking)
                    prediction_data = self.clf(text, candidate_labels)
                    # Transform to intent ranking format of rasa
                    new_intent_ranking = self.get_intent_ranking(prediction_data)
                    print("New intent rankings by bart")
                    print(new_intent_ranking)
                    if len(new_intent_ranking) > 0:
                        if new_intent_ranking[0]['name'] != 'other':  # if  new_intent_ranking[0] is other don't change
                            # remove 'other'
                            # Add as the new intent ranking
                            print("prediction of zero shot: ", new_intent_ranking[0])

                except Exception as e:
                    print(f"Failed to predict intent for text '{text}': {str(e)}")
        return messages

    @staticmethod
    def _get_training_data(training_data: TrainingData) -> set[Any]:
        """Preprocess the training data. Retrieve the text messages and their corresponding intents."""
        print("Getting training data for ZeroShotBartIntentClassifier")

        unique_intents = set()

        for example in training_data.training_examples:
            intent = example.get(INTENT)

            if intent and intent not in unique_intents:
                unique_intents.add(intent)
        return unique_intents

    @staticmethod
    def get_intent_ranking(prediction_data):
        # Create a list of tuples where each tuple is (label, score)
        label_score_pairs = list(zip(prediction_data['labels'], prediction_data['scores']))

        # Check the first label
        if label_score_pairs[0][1] > 0.9:
            selected_labels = [{'name': label_score_pairs[0][0], 'confidence': label_score_pairs[0][1]}]
        else:
            # Pick the highest scoring labels that sum up to at most 0.9
            selected_labels = []
            total_score = 0
            for label, score in label_score_pairs:
                if total_score + score <= 0.9:
                    selected_labels.append({'name': label, 'confidence': score})
                    total_score += score
                else:
                    break

        return selected_labels

    @staticmethod
    def get_candidate_labels(self, intent_ranking):
        num_intents = len(intent_ranking)
        clas_size = self.candidate_class_size
        num_intents_to_classify = num_intents if num_intents < clas_size else clas_size  # five top intents
        candidate_labels = [item['name'] for item in intent_ranking[:num_intents_to_classify]]
        candidate_labels.append('other')  # to catch out of scope
        return candidate_labels
