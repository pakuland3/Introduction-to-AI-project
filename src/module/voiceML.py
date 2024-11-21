# import os
import whisper
import librosa
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.metrics import accuracy_score
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
    max_length = 30 * 16000  # 30 seconds
    y = librosa.util.fix_length(y, size=max_length)  # Pad or trim to 30 seconds
    return y

def extract_whisper_features(audio):
    """
    Extract embeddings using Whisper's encoder.
    """
    mel = whisper.log_mel_spectrogram(audio)  # Generate log-Mel spectrogram
    mel = mel.unsqueeze(0)  # Add batch dimension to make it (1, n_mels, time_steps)
    
    with torch.no_grad():  # Disable gradient computation
        embeddings = model.encoder(mel.to(model.device))  # Pass through encoder
    
    # Use mean pooling along the time_steps dimension (dim=2)
    return embeddings.mean(dim=2).squeeze().cpu().numpy()  # Convert to NumPy


def getPrediction(path):
    # Load the saved model
    if __name__=="__main__":
        classifier = joblib.load("audio_classifier.pkl")
    else:
        classifier = joblib.load("src\\module\\audio_classifier.pkl")

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
data_dir = "..\\training sources"

# train session

# X, y = [], []
# for label, group in enumerate(["happy","sad","angry","anxious"]):
#     folder_path = os.path.join(data_dir, group)
#     for file_name in os.listdir(folder_path):
#         try:
#             audio = preprocess_audio(os.path.join(folder_path, file_name))
#             features = extract_whisper_features(audio)
#             X.append(features)
#             y.append(label)
#         except Exception as e:
#             print(f"Error processing {file_name}: {e}")

# # Convert to arrays
# X, y = np.array(X), np.array(y)

# # Split into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# # Train a Random Forest Classifier
# classifier = RandomForestClassifier(n_estimators=100, random_state=42)
# classifier.fit(X_train, y_train)

# # Make predictions and evaluate
# y_pred = classifier.predict(X_test)
# print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

# joblib.dump(classifier, "audio_classifier.pkl") # save model


# test session


# # Load the saved model
# classifier = joblib.load("audio_classifier.pkl")

# # Preprocess and extract features for the new audio
# audio = preprocess_audio("test-soon-2.wav")
# features = extract_whisper_features(audio)

# # Reshape the features and make a prediction
# features = features.reshape(1, -1)  # Ensure 2D input
# predicted_label = classifier.predict(features)

# # Map numeric label to class name
# label_mapping = {0: "happy", 1: "sad", 2: "angry", 3: "anxious"}
# print(f"Predicted class: {label_mapping[predicted_label[0]]}")


# "빠른 갈색 여우가 게으른 개를 뛰어넘습니다."

# "안녕하세요! 오늘 기분은 어떠신가요?"

# "머신 러닝 모델은 라벨이 지정된 데이터셋을 사용하여 학습됩니다."

# "오늘의 기온은 섭씨 23도입니다."

# "와, 이게 실제로 일어나다니 믿을 수 없어요!"