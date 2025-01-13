import torch
import librosa

emotions = ["neutral", "calm", "happy", "sad", "angry", "fear", "disgust", "surprised"]
scores = [40, 100, 50, 20, 30, 10, 5, 15]  # Assigning scores based on predefined criteria

def get_score(file_path, model, device):
    try:
        y, sr = librosa.load(file_path, sr=16000)  # Ensure 16kHz sampling rate

        # Convert to tensor and add batch dimension
        waveform = torch.tensor(y, dtype=torch.float32).unsqueeze(0).to(device)

        # Run inference
        with torch.no_grad():
            output = model(waveform)

        # Debug model output
        print(f"Model Output: {output}")

        # Post-process the output (e.g., softmax for classification)
        probabilities = torch.nn.functional.softmax(output, dim=1)

        # Debug probabilities
        print(f"Probabilities: {probabilities}")

        # Get the predicted class
        predicted_class = torch.argmax(probabilities, dim=1).item()
        print(f"Predicted Class: {predicted_class}", emotions[predicted_class], scores[predicted_class])
        return emotions[predicted_class], scores[predicted_class]

    except Exception as e:
        print(f"An error occurred: {e}")
        return f"Error: {e}", 0
