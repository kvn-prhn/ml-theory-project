from utils import log

input_model_path = './out/encounters_random_forest_model_2.joblib'
input_X_test_path = './out/encounters_random_forest_X_test.joblib'
input_y_test_path = './out/encounters_random_forest_y_test.joblib'

log("importing libraries")
import joblib
import numpy as np

log("loading model")
model = joblib.load(input_model_path)

log("loading test data")
X_test = joblib.load(input_X_test_path)
y_test = joblib.load(input_y_test_path)

log(f"Test accuracy: {model.score(X_test, y_test):.4f}")

log("Overall Feature GINI Scores")
importances = model.feature_importances_
sorted_indices = np.argsort(importances)[::-1]
for i in sorted_indices:
    if (not importances[i] == 0):
        print(f"{model.feature_names_in_[i]}: {importances[i]:.4f}")

original_features = ['Num Encounters', 'Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start']
grouped_importances = {feature: 0.0 for feature in original_features}

for i in range(len(model.feature_importances_)):
    feature_name_one_hot = model.feature_names_in_[i]
    feature_importance = model.feature_importances_[i]

    matched = False
    for original_feature in original_features:
        if feature_name_one_hot.startswith(original_feature):
            grouped_importances[original_feature] += feature_importance
            matched = True
            break
    
    if (not matched):
        raise Exception("feature not found: " + feature_name_one_hot)

log("Normalized Gini Importaces")
sorted_features = sorted(grouped_importances.items(), key=lambda x: x[1], reverse=True)
for feature, importance in sorted_features:
    log(f"{feature}: {importance:.4f}")