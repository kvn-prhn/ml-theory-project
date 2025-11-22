"""
RUN #1: baseline
- features: 'Num Encounters', 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start'
- target: 'Deported'
- Training accuracy: 0.8414
- Test accuracy: 0.8416

RUN #2: remove encounter date after start > 600
- features: 'Num Encounters', 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start'
- target: 'Deported'
- Training accuracy: 0.8561
- Test accuracy: 0.8569
"""

input_parquet = 'ice_data/clean_data/encounters.parquet'
model_path = './out/encounters_decision_tree_2.joblib'

from utils import log

log("import libraries")
import pandas as pd
import clean_encounters
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

log("reading in data")
df = pd.read_parquet(input_parquet)

log("combining rows with the same individual")
clean_encounters.combine_duplicate_ids(df)

log("drop 'Days After Start' > 600")
df.drop(df[df['Days After Start'] > 600].index, inplace=True)

features = ['Num Encounters', 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start']
target = 'Deported'

log("creating dummy variables")
X = pd.get_dummies(df[features], drop_first=True)
y = df[target]

log("test-train split")
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)

log("fitting decision tree")
model = DecisionTreeClassifier(random_state=1, max_depth=5)
model.fit(X_train, y_train)

log(f"Decision tree trained with {len(features)} features")
log(f"Training accuracy: {model.score(X_train, y_train):.4f}")
log(f"Test accuracy: {model.score(X_test, y_test):.4f}")
log("%d dummy variables" % len(X.columns))

log("storing model")
joblib.dump(model, model_path)

log("storing test data")
X_test_path = './out/encounters_decision_tree_X_test.joblib'
y_test_path = './out/encounters_decision_tree_y_test.joblib'
joblib.dump(X_test, X_test_path)
joblib.dump(y_test, y_test_path)