import vosk
import pyaudio
import json
import nltk
from nltk.corpus import cmudict
import pyttsx3
import os

# Ensure CMU Pronouncing Dictionary is downloaded
nltk.download('cmudict')
pron_dict = cmudict.dict()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Define a set of hardcoded words for testing
target_words = {"hello", "autism", "speech", "recognition", "python", "therapy"}

# Ensure Vosk model path is correct
model_path = "E:\\Studies\\Extra\\Competitions\\Ongoing\\Rugged\\ATD_SpeechTherapy\\model\\vosk_model"
if not os.path.exists(model_path):
    print("Error: Vosk model not found! Please check your model path.")
    exit(1)

# Load the Vosk speech recognition model
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Function to get phonemes of a word
def get_phonemes(word):
    return pron_dict.get(word.lower(), [])

# Function to check pronunciation
def check_pronunciation(spoken_word):
    if spoken_word in target_words:
        correct_phonemes = get_phonemes(spoken_word)
        if not correct_phonemes:
            return f"Pronunciation data not available for '{spoken_word}'."
        
        # Providing correct pronunciation
        phoneme_string = " ".join(correct_phonemes[0])
        return f"Correct pronunciation of '{spoken_word}': {phoneme_string}"
    
    return f"'{spoken_word}' is not in the predefined words list."

# Function to provide feedback
def provide_feedback(message):
    print(f"🔊 {message}")
    engine.say(message)
    engine.runAndWait()

# Start listening for speech input
print("\nListening for speech... Speak now!")

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

while True:
    data = stream.read(4000, exception_on_overflow=False)
    
    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "").strip().lower()

        if text:
            print(f"You said: {text}")

            # Split words and process each separately
            words = text.split()
            valid_words = [word for word in words if word in target_words]

            if valid_words:
                for word in valid_words:
                    feedback = check_pronunciation(word)
                    provide_feedback(feedback)
            else:
                provide_feedback(f"No correct words detected. Try again.")
        else:
            print("No speech detected. Try speaking clearly.")
