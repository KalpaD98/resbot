import logging
from typing import Dict, Text, Any, List, Type

from dotenv import load_dotenv
from rasa.engine.graph import GraphComponent, ExecutionContext
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.resource import Resource
from rasa.engine.storage.storage import ModelStorage
from rasa.nlu.classifiers.classifier import IntentClassifier
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
        return [IntentClassifier]

    @classmethod
    def required_packages(cls) -> List[Text]:
        """Any extra python dependencies required for this component to run."""
        return ['transformers']

    @staticmethod
    def get_default_config() -> Dict[Text, Any]:
        return {
            "threshold": 0.2,
            "ambiguity_threshold": 0.05,
            "candidate_class_size": 5,
            "top_intent_confidence_threshold": 0.9,
            "fallback_classifier_threshold": 0.3,  # must be same as the threshold given for fallback_classifier (fbc)
            "fallback_classifier_ambiguity_threshold": 0.1,  # must be same as the ambiguity threshold (fbc)
        }

    @classmethod
    def validate_config(cls, config: Dict[Text, Any]) -> None:
        """Validates that the component is configured properly."""
        pass

    def __init__(self, config: Dict[Text, Any], name: Text, model_storage: ModelStorage, resource: Resource) -> None:
        print("init ZeroShotBartIntentClassifier")
        self.name = name
        print("Init ZeroShotBartIntentClassifier and model")
        # TODO : pretrained below model in HFT
        self.clf = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
        self._model_storage = model_storage
        self._resource = resource

        self.threshold = config["threshold"]
        self.ambiguity_threshold = config["ambiguity_threshold"]

        self.candidate_class_size = config["candidate_class_size"]
        self.top_intent_confidence_threshold = config["top_intent_confidence_threshold"]

        self.fallback_classifier_threshold = config["fallback_classifier_threshold"]
        self.fallback_classifier_ambiguity_threshold = config["fallback_classifier_ambiguity_threshold"]

    @classmethod
    def create(
            cls,
            config: Dict[Text, Any],
            model_storage: ModelStorage,
            resource: Resource,
            execution_context: ExecutionContext,
    ) -> 'ZeroShotBartIntentClassifier':
        return cls(config, execution_context.node_name, model_storage, resource)

    def process(self, messages: List[Message]) -> List[Message]:
        """Process the list of messages."""
        # predict only if DIET fails
        print("\nProcess ZERO SHOT Bart Classifier")
        for message in messages:
            intent_ranking = message.get(INTENT_RANKING_KEY)
            intent = message.get(INTENT)

            print("\n----Intent Ranking from DIET classifier----\n")
            print(intent_ranking)
            print("\nDIET chosen intent: ", intent)
            print()

            text = message.get(TEXT)
            # check for intent being nlu_fallback if yes then run below code
            # can use this condition to control
            if self._should_classify_with_bart(self, text, intent_ranking):
                print("DIET failed to predict intent within given confidence. Trying to predict via bart\n")
                try:
                    # get from DIET and add from GPT pretrain and add other
                    candidate_labels = self._get_candidate_labels(self, intent_ranking)
                    print("text:", text)
                    prediction_data = self.clf(text, candidate_labels)
                    # Transform to intent ranking format of rasa
                    new_intent_ranking = self._get_bart_intent_ranking(self, prediction_data)
                    print("----- New intent rankings by bart zero shot -----\n")
                    print(new_intent_ranking)

                    if self._should_add_new_intent_rankings_to_tracker(self, new_intent_ranking):
                        print("prediction of zero shot: ", new_intent_ranking[0])
                        message.set(INTENT, new_intent_ranking[0], add_to_output=True)
                        message.set(INTENT_RANKING_KEY, new_intent_ranking, add_to_output=True)
                        print("updated the tracker with new intent ranking")
                    else:
                        print("Not adding to tracker: not enough confidence")
                # TODO: when 'haiya chatbot' is entered greet is not in intent ranking so still fail
                # TODO: when 'hiaya chatbot' is entered greet is in intent ranking
                #  however after sending it to ZSC confidence is < than fallback_classifier_threshold hence trigger nlu_fallback

                # TODO: if confidence is less than a certain value ask from user

                #             # Set the language entity
                #             # removed below for bug fixing
                #             entity = {
                #                 'value': language,
                #                 'confidence': 0.1,
                #                 'entity': 'language',
                #                 'extractor': 'LanguageHandler'
                #             }
                #             message.set("entities", [entity], add_to_output=True)

                except Exception as e:
                    print(f"Failed to predict intent by zero shot bart for text '{text}': {str(e)}")
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
    def _should_classify_with_bart(self, text, diet_intent_ranking):
        """Determines whether text should be classified with BART classifier based on DIET intent ranking and
        fallback classifier thresholds."""
        if text is None or diet_intent_ranking is None or len(diet_intent_ranking) == 0:
            return False

        top_intent = diet_intent_ranking[0]

        # Make sure there are at least two intents in the intent_ranking
        if len(diet_intent_ranking) < 2:
            return False
        second_top_intent = diet_intent_ranking[1]
        return (top_intent['confidence'] < self.fallback_classifier_threshold or
                (top_intent['confidence'] - second_top_intent['confidence'])
                < self.fallback_classifier_ambiguity_threshold)

    @staticmethod
    def _should_add_new_intent_rankings_to_tracker(self, bart_intent_ranking):
        """Determines whether text should be processed with BART classifier based on intent ranking and thresholds."""
        top_intent = bart_intent_ranking[0]
        meet_threshold_confidence = top_intent['confidence'] >= self.threshold
        if len(bart_intent_ranking) < 2:
            return meet_threshold_confidence
        else:
            second_top_intent = bart_intent_ranking[1]
            diff = top_intent['confidence'] - second_top_intent['confidence']
            meet_ambiguity_threshold_confidence = diff >= self.ambiguity_threshold
            return meet_threshold_confidence and meet_ambiguity_threshold_confidence

    @staticmethod
    def _get_bart_intent_ranking(self, prediction_data):
        """Transform the prediction data into the intent ranking format of rasa."""

        # Create a list of tuples where each tuple is (label, score)
        label_score_pairs = list(zip(prediction_data['labels'], prediction_data['scores']))

        # Check the first label
        if label_score_pairs[0][1] >= self.top_intent_confidence_threshold:
            new_intent_ranking = [{'name': label_score_pairs[0][0], 'confidence': label_score_pairs[0][1]}]
        else:
            # Pick the highest scoring labels that sum up to at most 0.99
            new_intent_ranking = []
            total_score = 0
            for label, score in label_score_pairs:
                if total_score + score <= 0.99:
                    new_intent_ranking.append({'name': label, 'confidence': score})
                    total_score += score
                else:
                    break
        if new_intent_ranking[0]['name'] == 'other':
            new_intent_ranking = []
        else:
            # Remove other
            new_intent_ranking = [intent for intent in new_intent_ranking if intent['name'] != 'other']

        return new_intent_ranking

    @staticmethod
    def _get_candidate_labels(self, intent_ranking):
        num_intents = len(intent_ranking)
        clas_size = self.candidate_class_size
        num_intents_to_classify = min(num_intents, clas_size)  # top intents
        candidate_labels = [item['name'] for item in intent_ranking[:num_intents_to_classify]]
        print("Pushing below labels to zero shot classifier")
        print("Candidate labels: ", candidate_labels)
        candidate_labels.append('other')  # to catch out of scope
        return candidate_labels

    # Unused methods
    #
    # @staticmethod
    # def compute_weighted_average(diet_intent_ranking, zero_shot_intent_ranking, weights):
    #     """
    #     Computes the weighted average of the confidence scores from the DIET and Zero-Shot classifiers.
    #
    #     :param diet_intent_ranking: The intent ranking from the DIET classifier.
    #     :param zero_shot_intent_ranking: The intent ranking from the Zero-Shot classifier.
    #     :param weights: The weights assigned to the DIET and Zero-Shot classifiers.
    #     :return: The intent ranking with confidence scores computed as the weighted average.
    #     """
    #     diet_confidences = {intent['name']: intent['confidence'] for intent in diet_intent_ranking}
    #     zero_shot_confidences = {intent['name']: intent['confidence'] for intent in zero_shot_intent_ranking}
    #
    #     averaged_confidences = {}
    #
    #     # Compute the weighted average for each intent.
    #     for intent in set(diet_confidences.keys()).union(zero_shot_confidences.keys()):
    #         diet_confidence = diet_confidences.get(intent, 0)
    #         zero_shot_confidence = zero_shot_confidences.get(intent, 0)
    #         averaged_confidences[intent] = diet_confidence * weights[0] + zero_shot_confidence * weights[1]
    #
    #     # Transform the dictionary back into a list of dictionaries.
    #     averaged_intent_ranking = [{'name': intent, 'confidence': confidence} for intent, confidence in
    #                                averaged_confidences.items()]
    #
    #     # Sort the intents by their confidence score in descending order.
    #     averaged_intent_ranking.sort(key=lambda intent: -intent['confidence'])
    #
    #     return averaged_intent_ranking
    #
    #     # TODO: USAGE
    #     # weighted_intent_ranking = self.compute_weighted_average(
    #     #     intent_ranking, new_intent_ranking,[0.5, 0.5])  # Adjust the weights as needed.
    #     # message.set(INTENT, weighted_intent_ranking[0], add_to_output=True)
    #     # message.set(INTENT_RANKING_KEY, weighted_intent_ranking, add_to_output=True)
    #
    # # TODO: test Softmax scoring method
    # @staticmethod
    # def softmax(x):
    #     """Compute softmax values for each sets of scores in x."""
    #     e_x = np.exp(x - np.max(x))
    #     return e_x / e_x.sum()
    #
    # @staticmethod
    # def postprocess_confidence_scores(self, intent_ranking):
    #     # Convert the confidence scores to a numpy array
    #     confidences = np.array([intent['confidence'] for intent in intent_ranking])
    #
    #     # Apply the softmax function
    #     softmax_confidences = self.softmax(confidences)
    #
    #     # Update the confidence scores in the intent ranking
    #     for i, intent in enumerate(intent_ranking):
    #         intent['confidence'] = softmax_confidences[i]
    #
    #     return intent_ranking
