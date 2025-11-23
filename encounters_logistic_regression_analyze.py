save_image = True
model_path = './out/encounters_logistic_regression_3.joblib'
X_test_path = './out/encounters_logistic_regression_X_test_3.joblib'
y_test_path = './out/encounters_logistic_regression_y_test_3.joblib'

from utils import log
log("importing libraries")
import joblib
from sklearn.linear_model import LogisticRegression

log("loading model")
model = joblib.load(model_path)

log("loading test data")
X_test = joblib.load(X_test_path)
y_test = joblib.load(y_test_path)

log(f"Test accuracy: {model.score(X_test, y_test):.4f}")

coefficients = model.coef_[0]
feature_names = model.feature_names_in_

coef_pairs = list(zip(feature_names, coefficients))
sorted_coefs = sorted(coef_pairs, key=lambda x: abs(x[1]), reverse=True)

log("Logistic Regression Coefficients:")
for feature, coef in sorted_coefs:
    log(f"{feature}: {coef:.4f}")
