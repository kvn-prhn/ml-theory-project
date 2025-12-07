model_path = './out/removals_lasso.joblib'
X_test_path = './out/removals_X_test.joblib'
y_test_path = './out/removals_y_test.joblib'

from utils import log
log("importing libraries")
import joblib
import numpy as np

log("loading model")
model = joblib.load(model_path)

log("loading test data")
X_test = joblib.load(X_test_path)
y_test = joblib.load(y_test_path)

log(f"Test accuracy (R^2): {model.score(X_test, y_test):.4f}")
log(f"Intercept: {model.intercept_:.4f}")

coefficients = model.coef_
feature_names = X_test.columns

coef_pairs = list(zip(feature_names, coefficients))
sorted_coefs = sorted(coef_pairs, key=lambda x: abs(x[1]), reverse=True)

log("linear regression coefficients")
for feature, coef in sorted_coefs:
    log(f"{feature}: {coef:.4f}")