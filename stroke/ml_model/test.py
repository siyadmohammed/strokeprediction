import pickle

MODEL_PATH = "stroke_backend\stroke\ml_model\decision_tree_model.pkl"

# Load model
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# Check the type of the model
print("Model Type:", type(model))