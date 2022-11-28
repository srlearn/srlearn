# Copyright © 2017-2021 Alexander L. Hayes

"""
Multiclass classification data transformers.
"""

import numpy as np
from sklearn.preprocessing import LabelEncoder
from relational_datasets.types import RelationalDataset


def _to_multiclass_vector(examples):
    # Convert a set of positive examples of the form `example(id,class).`
    # to a vector of the form `['2', '1', '0', '1']`

    labels = []

    for example in examples:
        _, body = example.split("(")
        values, _ = body.split(")")
        _, label = values.split(",")
        labels.append(label)

    return labels

def _multiclass_vector_to_dataset(dataset):
    # Convert a dataset + an encoded into K binary datasets

    labels = _to_multiclass_vector(dataset.pos)
    le = LabelEncoder()
    vector = le.fit_transform(labels)

    for c, _ in enumerate(le.classes_):
        pos = np.asarray(dataset.pos)[vector == c].tolist()
        neg = np.asarray(dataset.pos)[vector != c].tolist()

        yield RelationalDataset(pos, neg, dataset.facts)


class OneVsRestClassifier:

    def __init__(self, estimator, n_jobs=None):
        pass

    def fit(self, dataset):
        pass 

    def predict(self, dataset):
        pass

    def predict_proba(self, dataset):
        pass
