import vosk
import pyaudio
import json
import nltk
from nltk.corpus import cmudict
import pyttsx3
import os
import time
from difflib import get_close_matches

# Ensure CMU Pronouncing Dictionary is downloaded
nltk.download('cmudict')
pron_dict = cmudict.dict()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Define a set of hardcoded words for testing
target_words = {"hello", "autism", "speech", "recognition", "python", "therapy"}

# Human-friendly pronunciation guide
human_pronunciations = {
    "hello": "Say 'hello' like 'heh-low'.",
    "autism": "Say 'autism' like 'aw-tiz-um'.",
    "speech": "Say 'speech' like 'spee-ch'.",
    "recognition": "Say 'recognition' like 'rek-uhg-nish-uhn'.",
    "python": "Say 'python' like 'pie-thon'.",
    "therapy": "Say 'therapy' like 'thair-uh-pee'."
}

# Set the correct Vosk model path
model_path = "E:\\Studies\\Extra\\Competitions\\Ongoing\\Rugged\\ATD_SpeechTherapy\\model\\vosk_model"
if not os.path.exists(model_path):
    print("Error: Vosk model not found! Please check your model path.")
    exit(1)

# Load the Vosk speech recognition model
model = vosk.Model(model_path)
recognizer = vosk.KaldiRecognizer(model, 16000)

# Function to find the closest match for any spoken word
def get_closest_match(spoken_word):
    matches = get_close_matches(spoken_word, target_words, n=1, cutoff=0.5)  # Loose match to detect similarities
    return matches[0] if matches else None

# Function to check pronunciation and provide a natural explanation
def check_pronunciation(spoken_word):
    closest_match = get_closest_match(spoken_word)
    
    if closest_match:
        if spoken_word == closest_match:
            return f"'{spoken_word}' is pronounced correctly."
        else:
            return f"Almost there! You said '{spoken_word}', but try saying it like this: {human_pronunciations[closest_match]}"
    
    return f"'{spoken_word}' is not recognized. Try pronouncing a word similar to: {', '.join(target_words)}"

# Function to provide feedback without causing self-recognition
def provide_feedback(message):
    print(message)
    engine.say(message)
    engine.runAndWait()
    time.sleep(2)  # Prevents system voice from being taken as input

# Start listening for speech input
print("\nListening for speech... Say 'Begin' to start.")

pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

activation_confirmed = False
last_spoken_word = None  # Track last word to prevent repetition

while True:
    data = stream.read(4000, exception_on_overflow=False)

    if recognizer.AcceptWaveform(data):
        result = json.loads(recognizer.Result())
        text = result.get("text", "").strip().lower()

        if text:
            print(f"You said: {text}")

            # Require user to say "Begin" before processing any words
            if not activation_confirmed:
                if "begin" in text:
                    activation_confirmed = True
                    print("Activation confirmed. Please say a target word.")
                continue  # Ignore any other speech until "Begin" is spoken

            # Split words and process each one
            words = text.split()

            for word in words:
                if word != last_spoken_word:  # Avoid repeating feedback for the same word
                    feedback = check_pronunciation(word)
                    if feedback:
                        provide_feedback(feedback)
                    last_spoken_word = word  # Store last spoken word to prevent repetition
