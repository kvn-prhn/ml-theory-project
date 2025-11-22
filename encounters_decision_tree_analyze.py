save_image = True
model_path = './out/encounters_decision_tree_2.joblib'
X_test_path = './out/encounters_decision_tree_X_test.joblib'
y_test_path = './out/encounters_decision_tree_y_test.joblib'
output_image_path = 'out/encounters_decision_tree_2.png'

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

log(f"Test accuracy: {model.score(X_test, y_test):.4f}")

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
            class_names=['Not Deported', 'Deported'],
            filled=True,
            rounded=True,
            label='none',
            fontsize=7,
            impurity=False,  # Hide gini/entropy values
            proportion=True)  # Show proportions instead of sample counts
    plt.title("Decision Tree Classifier Visualization")
    plt.savefig(output_image_path, dpi=200, bbox_inches='tight')
    log("Tree visualization saved to %s" % output_image_path)