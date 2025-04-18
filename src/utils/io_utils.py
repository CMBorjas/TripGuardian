import os
import joblib

def save_model(model, path):
    """
    Saves a trained model to the specified path.

    Args:
        model: Trained model object (e.g., RandomForestRegressor).
        path (str): File path to save the model to.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"✅ Model saved to {path}")


def load_model(path):
    """
    Loads a model from the specified path.

    Args:
        path (str): Path to the saved model file.

    Returns:
        The loaded model object.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ Model file not found at: {path}")
    model = joblib.load(path)
    print(f"📦 Model loaded from {path}")
    return model
