# model.py

import os
import sys
import json
import numpy as np
import joblib
from spectral import open_image
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
import tensorflow as tf
import absl.logging
tf.config.set_visible_devices([], 'GPU')

# Suppress TensorFlow and Abseil logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
tf.get_logger().setLevel('ERROR')
absl.logging.set_verbosity(absl.logging.ERROR)

# Load models once
KMEANS_MODEL = 'kmeans_model.pkl'
PCA_MODEL = 'pca_model.pkl'
RF_MODEL = 'random_forest_moisture_model.pkl'
CNN_MODEL = 'piperine_prediction_cnn_model.h5'

try:
    kmeans = joblib.load(KMEANS_MODEL)
    pca_model = joblib.load(PCA_MODEL)
    rf_model = joblib.load(RF_MODEL)
    cnn_model = load_model(CNN_MODEL)
except Exception as e:
    print(json.dumps({"error": f"Model loading error: {str(e)}"}), file=sys.stderr)
    raise RuntimeError(f"Model loading error: {str(e)}")

def mask_black_pepper(image):
    """Apply KMeans clustering to create a binary mask for black pepper."""
    pixels = image[:, :, 140].reshape(-1, 1)
    labels = kmeans.predict(pixels).reshape(image.shape[0], image.shape[1])
    return labels == 0  # Assuming pepper is cluster 0

def predict_moisture(img_path, hdr_path):
    """Run moisture and piperine prediction pipeline."""
    try:
        # Redirect TensorFlow logs to stderr temporarily
        original_stdout = sys.stdout
        sys.stdout = sys.stderr

        # Load hyperspectral image
        image = open_image(hdr_path).load()
        clusters = mask_black_pepper(image)

        # Apply the mask
        masked_image = image * clusters[..., np.newaxis]

        # Normalize the image
        scaler = MinMaxScaler()
        reshaped_img = masked_image.reshape(-1, masked_image.shape[-1])
        normalized_img = scaler.fit_transform(reshaped_img)
        normalized_img = normalized_img.reshape(masked_image.shape)

        # Extract average spectrum
        avg_spectrum = np.mean(normalized_img, axis=(0, 1))

        # Apply PCA
        pca_transformed = pca_model.transform(avg_spectrum.reshape(1, -1))

        # Predict moisture and piperine
        moisture_prediction = rf_model.predict(pca_transformed)[0]
        piperine_prediction = cnn_model.predict(pca_transformed)[0][0]

        sys.stdout = original_stdout  # Restore stdout

        return {
            "moisture_prediction": float(moisture_prediction),
            "piperine_prediction": float(piperine_prediction)
        }

    except Exception as e:
        sys.stdout = original_stdout  # Restore stdout on error
        return {"error": str(e)}
