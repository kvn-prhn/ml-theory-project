save_image = True
model_path = './out/removals_decision_tree.joblib'
X_test_path = './out/removals_X_test.joblib'
y_test_path = './out/removals_y_test.joblib'
output_image_path = 'out/removals_decision_tree.png'

from utils import log
log("importing libraries")
import os
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import joblib
import numpy as np

log("loading model")
model = joblib.load(model_path)

log("loading test data")
X_test = joblib.load(X_test_path)
y_test = joblib.load(y_test_path)

log(f"Test accuracy (R^2): {model.score(X_test, y_test):.4f}")

log("Overall Feature GINI Scores")
importances = model.feature_importances_
sorted_indices = np.argsort(importances)[::-1]
for i in sorted_indices:
    if (not importances[i] == 0):
        print(f"{model.feature_names_in_[i]}: {importances[i]:.4f}")

if save_image:
    os.makedirs('out', exist_ok=True)
    plt.figure(figsize=(30, 20))
    plot_tree(model,
            feature_names=X_test.columns,
            filled=True,
            rounded=True,
            label='none',
            fontsize=12,
            impurity=False,  # Hide gini/entropy values
            proportion=True)  # Show proportions instead of sample counts
    plt.title("Decision Tree Classifier Visualization")
    plt.savefig(output_image_path, dpi=200, bbox_inches='tight')
    log("Tree visualization saved to %s" % output_image_path)



"""
this section copied from encounters_decision_tree_analyze.py only with different features, R^2, and input paths.
"""
from utils import log

input_model_path = './out/removals_decision_tree.joblib'
input_X_test_path = './out/removals_X_test.joblib'
input_y_test_path = './out/removals_y_test.joblib'

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

original_features = ['Days since Entry', 'Age', 'Port of Departure', 'Departure Country', 'Case Threat Level', 'Final Program', 'Male', 'Docket AOR']
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