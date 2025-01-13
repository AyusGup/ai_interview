import speech_recognition as sr

def convert_speech_to_text(file_path: str) -> str:
    # Initialize recognizer class (for recognizing the speech)
    recognizer = sr.Recognizer()
    
    # Open the audio file
    with sr.AudioFile(file_path) as source:
        # Adjust for ambient noise and listen to the file
        print("Audio file recorded")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)  # Capture the audio data from the file
    
    try:
        # Recognize the speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"Transcription: {text}")
        return text
    except sr.UnknownValueError:
        # Error: Could not understand the audio
        print("Google Web Speech API could not understand the audio.")
        return "Error: Could not understand the audio"
    except sr.RequestError as e:
        # Error: Could not request results from the Google Web Speech API
        print(f"Error with the Google Web Speech API request; {e}")
        return f"Error: Could not request results; {e}"
