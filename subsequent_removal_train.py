# %%
input_clean_parquet = 'ice_data/clean_data/removals.parquet'

import pandas as pd
import importlib
import clean_utils
import clean_removals
from utils import log
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.linear_model import Lasso
import joblib

# %%
importlib.reload(clean_utils)
importlib.reload(clean_removals)

# %%
log("reading in clean data")
df = pd.read_parquet(input_clean_parquet)

# %%
clean_removals.combine_duplicate_ids_duration(df)

# %%
log("Remove rows without entry date")
rows_before = df.shape[0]
df.dropna(subset=['Entry Date'], inplace=True)
df.reset_index(drop=True, inplace=True)
rows_after = df.shape[0]
log("Removed %d rows without entry date. %d remain" % (rows_before - rows_after, rows_after))

# %%
log("Creating 'Days since Entry' column")
df['Days since Entry'] = (df['Departed Date'] - df['Entry Date']).dt.days.astype('int32')
negative_count = (df['Days since Entry'] < 0).sum()
df = df[df['Days since Entry'] >= 0]
log("Dropped %d rows with negative 'Days since Entry'" % negative_count)
log("%d rows remain" % df.shape[0])

# %%
log("Creating 'Departure Days After Start' column")
START_DATE = pd.to_datetime('2023-09-01 00:00:00')
df['Departure Days After Start'] = (df['Departed Date'] - START_DATE).dt.days.astype('int32')

# %%
log("Creating 'Age' column")
df['Age'] = df['Departed Date'].dt.year.astype('int32') - df['Birth Year']

# %%
log("Saving histogram of days until removal")
bins = range(0, int(df['Days Until Subsequent Removal'].max()) + 10, 10)
plt.hist(df['Days Until Subsequent Removal'], bins=bins)
plt.xlabel('Days')
plt.ylabel('Frequency')
plt.title('Frequency of Elapsed Time Until Subsequent Removal')
output_image_path = 'out/subsequent_removal.png'
plt.savefig(output_image_path, dpi=200, bbox_inches='tight')

# %%
log("Make 'Case Threat Level' Categorical")
df['Case Threat Level'] = df['Case Threat Level'].fillna(4.0)
threat_level_map = {
    1.0: "Level 1: Aggravated Felony or Two Felonies",
    2.0: "Level 2: One Felony or Three Misdameanors",
    3.0: "Level 3: One Misdameanor",
    4.0: "Level 4: No Criminal Conviction"
}
df['Case Threat Level'] = df['Case Threat Level'].map(threat_level_map)
log("Converted 'Case Threat Level' to categorical")

# %%

# clean_utils.summarize_ordinal_column(df['Days since Entry'])
# clean_utils.summarize_ordinal_column(df['Departure Days After Start']) --> gives too much info ... 
# clean_utils.summarize_ordinal_column(df['Age'])
# clean_utils.summarize_categorical_column(df['Port of Departure']) # 110 values
# clean_utils.summarize_categorical_column(df['Departure Country']) # 52 values
# clean_utils.summarize_categorical_column(df['Case Threat Level']) # 4 values
# clean_utils.summarize_categorical_column(df['Final Program']) # 24 values
# clean_utils.summarize_categorical_column(df['Male']) # 2 values
# clean_utils.summarize_categorical_column(df['Docket AOR']) # 26 values
# clean_utils.summarize_categorical_column(df['Case Criminality']) # 3 values --> 'Case Threat Level' is better
# clean_utils.summarize_categorical_column(df['MSC NCIC Charge']) # 178 values, type of criminal offenses, 'Case Threat Level' is better


# %%
features = ['Days since Entry', 'Age', 'Port of Departure', 'Departure Country', 'Case Threat Level', 'Final Program', 'Male', 'Docket AOR']
target = 'Days Until Subsequent Removal'

log("creating dummy variables")
X = pd.get_dummies(df[features], drop_first=True) # drop first avoids multi-colinearity
y = df[target]

# %%

print("X shape: %d, %d" % X.shape)
print("Y shape: %d" % y.shape)

# %%
log("test-train split")
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)

# %%

log("storing test data")
X_test_path = './out/removals_X_test.joblib'
y_test_path = './out/removals_y_test.joblib'
joblib.dump(X_test, X_test_path)
joblib.dump(y_test, y_test_path)

# %%
log("fitting decision tree")
model = DecisionTreeRegressor(random_state=1, max_depth=5)
model.fit(X_train, y_train)

log(f"Decision tree trained with {len(features)} features")
log(f"Training accuracy (coefficient of determination R^2): {model.score(X_train, y_train):.4f}")
log(f"Test accuracy: (coefficient of determination R^2) {model.score(X_test, y_test):.4f}")
log("%d dummy variables" % len(X.columns))

log("storing model")
model_path = './out/removals_decision_tree.joblib'
joblib.dump(model, model_path)

# %%
log("fitting random forest")
model = RandomForestRegressor(n_jobs=4, verbose=1, random_state=1, max_depth=5)
model.fit(X_train, y_train)

log(f"Training accuracy: {model.score(X_train, y_train):.4f}")
log(f"Test accuracy: {model.score(X_test, y_test):.4f}")

log("storing model")
model_path = './out/removals_random_forest.joblib'
joblib.dump(model, model_path)

# %%
log("fitting linear model with regularization")
model = Lasso(random_state=1) 
model.fit(X_train, y_train)

log(f"Training accuracy (R^2): {model.score(X_train, y_train):.4f}")
log(f"Test accuracy (R^2): {model.score(X_test, y_test):.4f}")

log("storing model")
model_path = './out/removals_lasso.joblib'
joblib.dump(model, model_path)

# %%
log("fitting histogram-based gradient boosting")
model = HistGradientBoostingRegressor(random_state=1)
model.fit(X_train, y_train)

log(f"Training accuracy (R^2): {model.score(X_train, y_train):.4f}")
log(f"Test accuracy (R^2): {model.score(X_test, y_test):.4f}")

log("storing model")
model_path = './out/removals_hist_gradient_boosting.joblib'
joblib.dump(model, model_path)

# ARCHIVE
# %%
# log("Remove rows without Most Serious Conviction (MSC)")
# rows_before = df.shape[0]
# df.dropna(subset=['MSC Conviction Date'], inplace=True)
# df.reset_index(drop=True, inplace=True)
# rows_after = df.shape[0]
# log("Removed %d rows without MSC convicion. %d remain" % (rows_before - rows_after, rows_after))

# %%
# log("Creating 'Days since MSC' column")
# df['Days since MSC'] = (df['Departed Date'] - df['MSC Conviction Date']).dt.days.astype('int32')
# negative_count = (df['Days since MSC'] < 0).sum()
# df = df[df['Days since MSC'] >= 0]
# print(f"Dropped {negative_count} rows with negative 'Days since MSC'")

# log("Remove rows without 'Case Threat Level'")
# rows_before = df.shape[0]
# df.dropna(subset=['Case Threat Level'], inplace=True)
# df.reset_index(drop=True, inplace=True)
# rows_after = df.shape[0]
# log("Removed %d rows without 'Case Threat Level'. %d remain" % (rows_before - rows_after, rows_after))