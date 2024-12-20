import librosa
import joblib
from whisper import log_mel_spectrogram, load_model
import torch

# Load the Whisper model
model = load_model("base")

def preprocess_audio(file_path):
    """
    Load and preprocess audio using librosa.
    """
    y, _ = librosa.load(file_path, sr=16000)  # Load audio and resample to 16 kHz
    # Pad or trim to 30 seconds
    max_length = 30 * 16000  # 30 seconds
    y = librosa.util.fix_length(y, size=max_length)
    return y

def extract_whisper_features(audio):
    """
    Extract embeddings using Whisper's encoder.
    """
    mel = log_mel_spectrogram(audio)  # Generate log-Mel spectrogram
    mel = mel.unsqueeze(0)  # Add batch dimension to make it (1, n_mels, time_steps)
    
    with torch.no_grad():  # Disable gradient computation
        embeddings = model.encoder(mel.to(model.device))  # Pass through encoder
    
    # Use mean pooling along the time_steps dimension (dim=2)
    return embeddings.mean(dim=2).squeeze().cpu().numpy()  # Convert to NumPy


def getPrediction(path):
    # Load the saved model
    classifier = joblib.load("src\\module\\audio_classifier_ver_last.pkl")

    # Preprocess and extract features for the new audio
    if path:
        audio = preprocess_audio(path)
        features = extract_whisper_features(audio)

        # Reshape the features and make a prediction
        features = features.reshape(1, -1)  # Ensure 2D input
        predicted_label = classifier.predict(features)

        # Map numeric label to class name
        label_mapping = {0: "happy", 1: "sad", 2: "angry", 3: "anxious"}
        return label_mapping[predicted_label[0]]

# Load your dataset
data_dir = "src\\training sources"



# train session

if __name__=="__main__":
    import os
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import accuracy_score
    import numpy as np
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

    joblib.dump(classifier, "audio_classifier.pkl") # save models