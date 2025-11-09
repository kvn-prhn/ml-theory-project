# %% ARGS

output_image_path = 'out/encounters_decision_tree.png'
input_parquet = 'ice_data/clean_data/encounters.parquet'

# %%
from utils import log

log("importing ML libraries")
import pandas as pd
import clean_utils
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree

df = pd.read_parquet(input_parquet)

# features = ['Gender', 'Days After Start', 'Encounter Criminality']
features = ['Responsible AOR', 'Event Type', 'Final Program', 'Encounter Criminality', 'Birth Year', 'Citizenship Country', 'Gender', 'Days After Start']
target = 'Deported'

log("creating dummy variables")
X = pd.get_dummies(df[features], drop_first=True)
y = df[target]

log("fitting decision tree")
model = DecisionTreeClassifier(random_state=42, max_depth=5)
model.fit(X, y)

log(f"Decision tree trained with {len(features)} features")
log(f"Training accuracy: {model.score(X, y):.4f}")
log("%d dummy variables" % len(X.columns))


# %%
import os
os.makedirs('out', exist_ok=True)

plt.figure(figsize=(30, 20))
plot_tree(model,
          feature_names=X.columns,
          class_names=['Not Deported', 'Deported'],
          filled=True,
          rounded=True,
          label='none',
          fontsize=7,
          impurity=False,  # Hide gini/entropy values
          proportion=True)  # Show proportions instead of sample counts
plt.title("Decision Tree Classifier Visualization")
# plt.show()
plt.savefig(output_image_path, dpi=200, bbox_inches='tight')
log("Tree visualization saved to %s" % output_image_path)
