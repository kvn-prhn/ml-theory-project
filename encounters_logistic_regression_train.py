"""
logistic regression sklearn api: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html#sklearn.linear_model.LogisticRegression

todo
- train logistic regression
- regularize

could do
- fancy plot of regularization: https://scikit-learn.org/stable/auto_examples/linear_model/plot_logistic_path.html#sphx-glr-auto-examples-linear-model-plot-logistic-path-py

RUN #1: 
- LogisticRegression()
- drop days after start > 600
- combine duplicate ids
- features: 'Num Encounters', 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start'
- no normalization
- Training accuracy: 0.8621
- Test accuracy: 0.8629
- sklearn normalization warning
- reached default limit of 100 iterations
- default regularization (l2 -- ridge)

RUN #2:
- Same as run 1 with normalizing quantitative variables
- Training accuracy: 0.8680
- Test accuracy: 0.8685
- default regularization (l2 -- ridge)

RUN #3:
- same as run 2, but l1 (lasso) regularization
- Training accuracy: 0.8681
- Test accuracy: 0.8686
"""

input_parquet = 'ice_data/clean_data/encounters.parquet'
model_path = './out/encounters_logistic_regression_3.joblib'

from utils import log

log("import libraries")
import pandas as pd
import clean_encounters
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib

log("reading in data")
df = pd.read_parquet(input_parquet)

log("combining rows with the same individual")
clean_encounters.combine_duplicate_ids(df)

log("drop 'Days After Start' > 600")
df.drop(df[df['Days After Start'] > 600].index, inplace=True)

log("normalize quantitative variables")
scaler = StandardScaler()
quantitative_features = ['Num Encounters', 'Birth Year', 'Days After Start']
df[quantitative_features] = scaler.fit_transform(df[quantitative_features])

features = ['Num Encounters', 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start']
target = 'Deported'

log("creating dummy variables")
X = pd.get_dummies(df[features], drop_first=True)
y = df[target]

log("test-train split")
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)

log("fitting logistic regression")
model = LogisticRegression(solver='liblinear', penalty='l1')
model.fit(X_train, y_train)

log("Training logistic regression")
log(f"Training accuracy: {model.score(X_train, y_train):.4f}")
log(f"Test accuracy: {model.score(X_test, y_test):.4f}")
log("%d dummy variables" % len(X.columns))

log("storing model")
joblib.dump(model, model_path)

log("storing test data")
X_test_path = './out/encounters_logistic_regression_X_test_3.joblib'
y_test_path = './out/encounters_logistic_regression_y_test_3.joblib'
joblib.dump(X_test, X_test_path)
joblib.dump(y_test, y_test_path)