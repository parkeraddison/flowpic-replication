import src

import pandas as pd
import numpy as np

import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from tensorflow import keras

import ast

def train(source, classifier, parameters):

    data = pd.read_csv(source)

    signals = data.signal.apply(ast.literal_eval)
    # Get series of tuples into the correct dimensions (n, 1, tuple_length)
    X = np.array([
        np.array(s, ndmin=2) for s in signals
    ])
    y = (data.activity.values == 'streaming').astype('int32')

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    model = keras.Sequential()
    model.add(keras.layers.LSTM(100))
    model.add(keras.layers.Dense(30))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    model.fit(X_train, y_train, epochs=5)

    # Evaluate on test (validation) data
    preds = (model.predict(X_test) > 0.5).astype('int32')

    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
    print('Accuracy:', accuracy_score(preds, y_test))
    print('F1:      ', f1_score(preds, y_test))
    print('ROC AUC: ', roc_auc_score(preds, y_test))
    print('')
    print('Predicted Browsing / Streaming ->')
    print('True Browsing / Streaming v')
    print(confusion_matrix(y_test, preds))

# def train(source, classifier, parameters):

#     data = pd.read_csv(source)

#     X = data.drop(columns=['file', 'activity'])
#     y = data.activity == 'streaming'

#     X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)


#     classifier_map = {
#         "RandomForest": RandomForestClassifier
#     }
#     params = parameters[classifier]
#     clf = classifier_map[classifier](**params)

#     clf.fit(X_train, y_train)

#     print(f"ROC AUC: {roc_auc_score(y_test, clf.predict(X_test))}")
