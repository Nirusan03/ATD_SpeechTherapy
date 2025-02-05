import vosk
import pyaudio
import json
import nltk
from nltk.corpus import cmudict
import pyttsx3
import os
import time
from difflib import get_close_matches

class PronunciationTrainer:
    def __init__(self, model_path):
        # Load CMU Pronouncing Dictionary
        nltk.download('cmudict')
        self.pron_dict = cmudict.dict()

        # Initialize text-to-speech engine
        self.engine = pyttsx3.init()

        # Define a set of hardcoded words for testing
        self.target_words = {"hello", "autism", "speech", "recognition", "python", "therapy"}

        # Human-friendly pronunciation guide
        self.human_pronunciations = {
            "hello": "Say 'hello' like 'heh-low'.",
            "autism": "Say 'autism' like 'aw-tiz-um'.",
            "speech": "Say 'speech' like 'spee-ch'.",
            "recognition": "Say 'recognition' like 'rek-uhg-nish-uhn'.",
            "python": "Say 'python' like 'pie-thon'.",
            "therapy": "Say 'therapy' like 'thair-uh-pee'."
        }

        # Load Vosk Model
        if not os.path.exists(model_path):
            raise FileNotFoundError("Error: Vosk model not found! Please check your model path.")
        self.model = vosk.Model(model_path)
        self.recognizer = vosk.KaldiRecognizer(self.model, 16000)

        # Initialize microphone
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        self.stream.start_stream()

        self.activation_confirmed = False
        self.last_spoken_word = None  # Track the last word spoken to avoid repetition

    def get_phonemes(self, word):
        """Returns the phonemes for a given word from CMU Pronouncing Dictionary."""
        return self.pron_dict.get(word.lower(), [])

    def get_closest_match(self, spoken_word):
        """Finds the closest word match from the predefined list."""
        matches = get_close_matches(spoken_word, self.target_words, n=1, cutoff=0.5)
        return matches[0] if matches else None

    def check_pronunciation(self, spoken_word):
        """Checks pronunciation and provides human-friendly guidance."""
        closest_match = self.get_closest_match(spoken_word)
        
        if closest_match:
            if spoken_word == closest_match:
                return f"'{spoken_word}' is pronounced correctly."
            else:
                return f"Almost there! You said '{spoken_word}', but try saying it like this: {self.human_pronunciations[closest_match]}"
        
        return f"'{spoken_word}' is not recognized. Try pronouncing a word similar to: {', '.join(self.target_words)}"

    def provide_feedback(self, message):
        """Provides verbal and printed feedback."""
        print(message)
        self.engine.say(message)
        self.engine.runAndWait()
        time.sleep(2)  # Prevents system voice from being taken as input

    def listen_and_process(self):
        """Main loop for processing speech input."""
        print("\nListening for speech... Say 'Begin' to start.")

        while True:
            data = self.stream.read(4000, exception_on_overflow=False)

            if self.recognizer.AcceptWaveform(data):
                result = json.loads(self.recognizer.Result())
                text = result.get("text", "").strip().lower()

                if text:
                    print(f"You said: {text}")

                    # Require user to say "Begin" before processing any words
                    if not self.activation_confirmed:
                        if "begin" in text:
                            self.activation_confirmed = True
                            print("Activation confirmed. Please say a target word.")
                        continue  # Ignore any other speech until "Begin" is spoken

                    # Split words and process each one
                    words = text.split()

                    for word in words:
                        if word != self.last_spoken_word:  # Avoid repeating feedback for the same word
                            feedback = self.check_pronunciation(word)
                            if feedback:
                                self.provide_feedback(feedback)
                            self.last_spoken_word = word  # Store last spoken word to prevent repetition


if __name__ == "__main__":
    # Path to your Vosk model
    MODEL_PATH = "E:\\Studies\\Extra\\Competitions\\Ongoing\\Rugged\\ATD_SpeechTherapy\\model\\vosk_model"

    trainer = PronunciationTrainer(MODEL_PATH)
    trainer.listen_and_process()
