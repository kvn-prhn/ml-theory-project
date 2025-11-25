"""
RUN #1: Baseline
- features: 'Num Encounters', 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start'
- target: 'Deported'
- test_train_split(stratify=y)
- Training accuracy: 0.9985
- Test accuracy: 0.8688

RUN #2: Only keep first 600 days of data
"""

intput_data_path = 'ice_data/clean_data/encounters.parquet'
output_model_path = './out/encounters_random_forest_model_2.joblib'
output_X_test_path = './out/encounters_random_forest_X_test.joblib'
output_y_test_path = './out/encounters_random_forest_y_test.joblib'

from utils import log

log("importing libraries")
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import clean_encounters
import joblib


log("loading clean data")
df = pd.read_parquet(intput_data_path)

log("combining rows with the same individual")
clean_encounters.combine_duplicate_ids(df)

log("drop 'Days After Start' > 600")
df.drop(df[df['Days After Start'] > 600].index, inplace=True)

features = ['Num Encounters', 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start']
target = 'Deported'

log("one-hot encoding")
# drop_first removes one of the dummy variables to avoid multi-collinearity
X = pd.get_dummies(df[features], drop_first=True)
y = df[target]
log("%d features in new set" % len(X.columns))

log("test-train split")
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)

log("fitting random forest")
model = RandomForestClassifier(n_jobs=4, verbose=1, random_state=1)
model.fit(X_train, y_train)

log(f"Training accuracy: {model.score(X_train, y_train):.4f}")
log(f"Test accuracy: {model.score(X_test, y_test):.4f}")

log("storing model")
joblib.dump(model, output_model_path)

log("storing test data")
joblib.dump(X_test, output_X_test_path)
joblib.dump(y_test, output_y_test_path)

print(model.feature_importances_)