import random
from abc import ABC, abstractmethod
from collections import Counter
from typing import Optional, Union, List, Any

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, ClassifierMixin
from skllm.openai.chatgpt import (
    construct_message,
    get_chat_completion,
    extract_json_key,
)
from skllm.openai.mixin import OpenAIMixin as _OAIMixin
from skllm.utils import to_numpy as _to_numpy
from tqdm import tqdm


class _BaseZeroShotGPTClassifier(ABC, BaseEstimator, ClassifierMixin, _OAIMixin):
    def __init__(
            self,
            openai_key: Optional[str] = None,
            openai_org: Optional[str] = None,
            openai_model: str = "gpt-3.5-turbo",
    ):
        self._set_keys(openai_key, openai_org)
        self.openai_model = openai_model

    def _to_np(self, X):
        return _to_numpy(X)

    def fit(
            self,
            X: Optional[Union[np.ndarray, pd.Series, List[str]]],
            y: Union[np.ndarray, pd.Series, List[str], List[List[str]]],
    ):
        X = self._to_np(X)
        self.classes_, self.probabilities_ = self._get_unique_targets(y)
        return self

    def predict(self, X: Union[np.ndarray, pd.Series, List[str]]):
        X = self._to_np(X)
        predictions = []
        for i in tqdm(range(len(X))):
            predictions.append(self._predict_single(X[i]))
        return predictions

    def predict_single(self, X: Optional[str]):
        prediction = self._predict_single(X)
        return [prediction]

    @abstractmethod
    def _extract_labels(self, y: Any) -> List[str]:
        pass

    def _get_unique_targets(self, y):
        labels = self._extract_labels(y)

        counts = Counter(labels)

        total = sum(counts.values())

        classes, probs = [], []
        for l, c in counts.items():
            classes.append(l)
            probs.append(c / total)

        return classes, probs

    def _get_chat_completion(self, x):
        prompt = self._get_prompt(x)
        msgs = []
        msgs.append(construct_message("system", "You are a text classification model."))
        msgs.append(construct_message("user", prompt))
        completion = get_chat_completion(
            msgs, self._get_openai_key(), self._get_openai_org(), self.openai_model
        )
        return completion


class FewShotGPTClassifier(ABC, BaseEstimator, ClassifierMixin, _OAIMixin):
    def __init__(
            self,
            openai_key: Optional[str] = None,
            openai_org: Optional[str] = None,
            openai_model: str = "gpt-3.5-turbo",
    ):
        self._set_keys(openai_key, openai_org)
        self.openai_model = openai_model

    def _to_np(self, X):
        return _to_numpy(X)

    def fit(
            self,
            X: Optional[Union[np.ndarray, pd.Series, List[str]]],
            y: Union[np.ndarray, pd.Series, List[str], List[List[str]]],
    ):
        X = self._to_np(X)
        self.examples_ = {label: examples for label, examples in zip(X, y)}
        self.classes_, self.probabilities_ = self._get_unique_targets(y)
        return self

    def predict(self, X: Union[np.ndarray, pd.Series, List[str]], n_best: int = 5):
        X = self._to_np(X)
        predictions = []
        for i in tqdm(range(len(X))):
            predictions.append(self._predict_single(X[i], n_best))
        return predictions

    def predict_single(self, X: Optional[str], n_best: int = 5):
        prediction = self._predict_single(X, n_best)
        return [prediction]

    def _get_unique_targets(self, y):
        labels = list(self.examples_.keys())

        counts = Counter(labels)

        total = sum(counts.values())

        classes, probs = [], []
        for l, c in counts.items():
            classes.append(l)
            probs.append(c / total)

        return classes, probs

    def _get_chat_completion(self, x):
        examples = random.choices(list(self.examples_.items()), k=5)
        msgs = []
        msgs.append(construct_message("system", "You are a text classification model."))
        for label, examples in examples:
            for example in examples:
                msgs.append(construct_message("user", example))
                msgs.append(construct_message("assistant", label))
        msgs.append(construct_message("user", x))
        completion = get_chat_completion(
            msgs, self._get_openai_key(), self._get_openai_org(), self.openai_model
        )
        return completion

    def _predict_single(self, x, n_best):
        completion = self._get_chat_completion(x)
        try:
            scores = extract_json_key(completion.choices[0].message["content"], "scores")
            labels = extract_json_key(completion.choices[0].message["content"], "labels")
        except Exception as e:
            scores = []
            labels = []

        prediction = sorted(zip(labels, scores), key=lambda x: x[1], reverse=True)[:n_best]
        return prediction

    def fit(
            self,
            X: Optional[Union[np.ndarray, pd.Series, List[str]]],
            y: Union[np.ndarray, pd.Series, List[List[str]]],
    ):
        y = self._to_np(y)
        return super().fit(X, y)
