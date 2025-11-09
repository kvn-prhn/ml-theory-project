"""
RUN #1
- features: 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start'
- test_train_split(stratify=y)
- Training accuracy: 0.9928
- Test accuracy: 0.8413

todo:
- try this after combining rows with the same id, and use # encounters as a feature
- add encounter month (would be last encounter month)
"""

from utils import log

log("importing ML libraries")
import pandas as pd
import clean_utils
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

log("loading clean data")
df = pd.read_parquet('ice_data/clean_data/encounters.parquet')

features = ['Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start']
target = 'Deported'

log("one-hot encoding")
# drop_first removes one of the dummy variables to avoid multi-collinearity
X = pd.get_dummies(df[features], drop_first=True)
y = df[target]
log("%d features in new set" % len(X.columns))

log("test-train split")
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y)

log("fitting random forest")
model = RandomForestClassifier(n_jobs=4, verbose=1)
model.fit(X_train, y_train)

log(f"Training accuracy: {model.score(X_train, y_train):.4f}")
log(f"Test accuracy: {model.score(X_test, y_test):.4f}")
