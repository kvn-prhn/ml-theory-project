model_path = './out/removals_hist_gradient_boosting.joblib'
X_test_path = './out/removals_X_test.joblib'
y_test_path = './out/removals_y_test.joblib'

from utils import log
log("importing libraries")
import joblib
import numpy as np
from sklearn.inspection import permutation_importance

log("loading model")
model = joblib.load(model_path)

log("loading test data")
X_test = joblib.load(X_test_path)
y_test = joblib.load(y_test_path)

log(f"Test accuracy (R^2): {model.score(X_test, y_test):.4f}")

log("Computing permutation importance")
perm_importance = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=1)

log("Overall Feature Importance Scores")
importances = perm_importance.importances_mean
feature_names = X_test.columns
sorted_indices = np.argsort(importances)[::-1]
for i in sorted_indices:
    if (not importances[i] == 0):
        print(f"{feature_names[i]}: {importances[i]:.4f}")

original_features = ['Days since Entry', 'Age', 'Port of Departure', 'Departure Country', 'Case Threat Level', 'Final Program', 'Male', 'Docket AOR']
grouped_importances = {feature: 0.0 for feature in original_features}

for i in range(len(importances)):
    feature_name_one_hot = feature_names[i]
    feature_importance = importances[i]

    for original_feature in original_features:
        if feature_name_one_hot.startswith(original_feature):
            grouped_importances[original_feature] += feature_importance
            matched = True
            break

log("Grouped Feature Importances")
sorted_features = sorted(grouped_importances.items(), key=lambda x: x[1], reverse=True)
for feature, importance in sorted_features:
    print(f"{feature}: {importance:.4f}")