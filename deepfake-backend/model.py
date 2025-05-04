import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array, load_img
import os

# Load your trained model
MODEL_PATH = "Xception_model.keras"
model = load_model(MODEL_PATH)

# Set input size based on how the model was trained (224x224)
INPUT_SIZE = (224, 224)

# Function to extract frames from video
def extract_frames(video_path, max_frames=5):
    frames = []
    cap = cv2.VideoCapture(video_path)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    for i in range(min(max_frames, total)):
        cap.set(cv2.CAP_PROP_POS_FRAMES, i * (total // max_frames))
        ret, frame = cap.read()
        if ret:
            frame = cv2.resize(frame, INPUT_SIZE)
            frame = img_to_array(frame) / 255.0
            frames.append(frame)

    cap.release()
    return np.array(frames)

# Unified inference function
def run_inference(file_path):
    try:
        if file_path.lower().endswith(('.mp4', '.mov', '.avi')):
            frames = extract_frames(file_path)
            if len(frames) == 0:
                return "Error", 0
            preds = model.predict(frames)
            avg_confidence = float(np.mean(preds)) * 100
        else:
            img = load_img(file_path, target_size=INPUT_SIZE)
            img_array = img_to_array(img) / 255.0
            img_array = np.expand_dims(img_array, axis=0)
            preds = model.predict(img_array)
            avg_confidence = float(preds[0][0]) * 100

        result = "Fake" if avg_confidence > 50 else "Real"
        return result, round(avg_confidence, 2)

    except Exception as e:
        print(f"🔥 Inference Error: {e}")
        return "Error", 0
