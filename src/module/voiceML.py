import os
import whisper
import librosa
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import torch
import numpy as np
import joblib
# Load the Whisper model
model = whisper.load_model("base")

def preprocess_audio(file_path):
    """
    Load and preprocess audio using librosa.
    """
    y, _ = librosa.load(file_path, sr=16000)  # Load audio and resample to 16 kHz
    return y

def extract_whisper_features(audio):
    """
    Extract embeddings using Whisper's encoder.
    """
    mel = whisper.log_mel_spectrogram(audio)
    with torch.no_grad(): # torch.no_grad() -> for fast computation with with syntax
        embeddings = model.encode(mel)
    return embeddings.mean(dim=1).squeeze().numpy()  # Use mean pooling

# Load your dataset
data_dir = "src\\voices"

X, y = [], []
for label, group in enumerate(["happy","sad","angry","anxious"]):
    folder_path = os.path.join(data_dir, group)
    for file_name in os.listdir(folder_path):
        try:
            audio = preprocess_audio(os.path.join(folder_path, file_name))
            features = extract_whisper_features(audio)
            X.append(features)
            y.append(label)
        except Exception as e:
            print(f"Error processing {file_name}: {e}")

# Convert to arrays
X, y = np.array(X), np.array(y)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
classifier = RandomForestClassifier(n_estimators=100, random_state=42)
classifier.fit(X_train, y_train)

# Make predictions and evaluate
y_pred = classifier.predict(X_test)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

joblib.dump(classifier, "audio_classifier.pkl")