from utils import log

log("importing libraries")
import joblib

log("loading model")
model = joblib.load('./out/encounters_random_forest_model_1.joblib')

log("loading test data")
X_test = joblib.load('./out/encounters_random_forest_X_test.joblib')
y_test = joblib.load('./out/encounters_random_forest_y_test.joblib')

log(f"Test accuracy: {model.score(X_test, y_test):.4f}")

