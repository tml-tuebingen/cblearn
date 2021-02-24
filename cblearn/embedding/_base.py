from typing import Optional

import numpy as np
from sklearn.base import TransformerMixin
from sklearn.utils.validation import check_is_fitted

from cblearn import datasets
from cblearn import utils


class TripletEmbeddingMixin(TransformerMixin):
    def _more_tags(self):
        return {
            'requires_positive_X': True,
            'requires_positive_y': True,
            'X_types': ['categorical'],
        }

    def transform(self, X: Optional[utils.Questions] = None, y: Optional[np.ndarray] = None) -> np.ndarray:
        check_is_fitted(self, 'embedding_')
        return self.embedding_

    def predict(self, X: utils.Questions) -> np.ndarray:
        check_is_fitted(self, 'embedding_')
        return datasets.triplet_answers(X, self.embedding_)

    def score(self, X: utils.Questions, y: Optional[np.ndarray] = None) -> float:
        """ Triplet score on the estimated embedding.

        Args:
            X: Triplet answers
        Returns.
            Fraction of correct triplets.
        """
        from ..metrics import triplet_error

        if y is None:
            y = X
        return 1 - triplet_error(self.predict(X), y)