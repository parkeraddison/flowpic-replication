import src

import pandas as pd

import sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

def train(source, classifier, parameters):

    data = pd.read_csv(source)

    X = data.drop(columns=['file', 'activity'])
    y = data.activity == 'streaming'

    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)


    classifier_map = {
        "RandomForest": RandomForestClassifier
    }
    params = parameters[classifier]
    clf = classifier_map[classifier](**params)

    clf.fit(X_train, y_train)

    print(f"ROC AUC: {roc_auc_score(y_test, clf.predict(X_test))}")
