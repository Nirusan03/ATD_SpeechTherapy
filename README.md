# 🗣️ Pronunciation Trainer for Autism Support

A Python-based speech pronunciation trainer designed to help individuals, especially those with autism, improve their pronunciation using offline speech recognition. The system compares spoken words with a predefined list, identifies mispronunciations, and provides **human-friendly pronunciation guidance**.

## 🚀 Features
- 🎤 **Offline Speech Recognition** using **Vosk API**.
- 🔍 **Pronunciation Detection** for specific predefined words.
- 🤖 **Text-to-Speech Feedback** to guide users in a **human-friendly** manner.
- 🧠 **Machine Learning Approach** for word similarity detection.
- 🚫 **Prevents System Voice Misinterpretation** (does not detect its own output).
- 🔄 **Real-Time Listening & Feedback Loop**.

---

## 📌 Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [System Requirements](#system-requirements)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## 🛠 Installation

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/PronunciationTrainer.git
cd PronunciationTrainer
```

### **2️⃣ Install Required Dependencies**
```bash
pip install vosk pyaudio nltk pyttsx3
```

### **3️⃣ Download & Extract the Vosk Model**
```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d model
```

Alternatively, **manually download** the model from [Vosk Models](https://alphacephei.com/vosk/models) and extract it into the `model/` folder.

### **4️⃣ Run the Application**
```bash
python ASD_Speech.py
```

---

## 🎤 Usage
### **1️⃣ Start the Application**
Run the script and wait for **"Listening for speech... Say 'Begin' to start."**
```bash
python ASD_Speech.py
```

### **2️⃣ Say "Begin" to Activate**
Once the system is running, say:
```text
"Begin"
```
This will activate the pronunciation trainer.

### **3️⃣ Speak a Word**
- The system will **compare your spoken word** to predefined words.
- If your pronunciation is correct, it will confirm.
- If incorrect, it will **guide you on how to say it properly**.

### **Example Output**
#### ✅ Correct Pronunciation:
🗣️ **You say:** `"hello"`
```
You said: hello
'hello' is pronounced correctly.
```

#### ❌ Mispronounced Word:
🗣️ **You say:** `"lo"` (Trying to say "hello")
```
You said: lo
Almost there! You said 'lo', but try saying it like this: Say 'hello' like 'heh-low'.
```

#### ❌ Unrecognized Word:
🗣️ **You say:** `"regulation"`
```
You said: regulation
'regulation' is not recognized. Try pronouncing a word similar to: hello, autism, speech, recognition, python, therapy.
```

---

## ⚙️ Configuration
The predefined words **can be modified** inside `ASD_Speech.py`:
```python
self.target_words = {"hello", "autism", "speech", "recognition", "python", "therapy"}
```
To **add new words**, simply include them in `self.target_words` and update the `self.human_pronunciations` dictionary.

---

## 💻 System Requirements

| Component         | Requirement |
|------------------|------------|
| 🛠 **OS**         | Windows, Linux, macOS |
| 🐍 **Python**     | 3.7+ |
| 🎤 **Microphone** | Required for speech input |
| 📦 **Dependencies** | `vosk`, `pyaudio`, `nltk`, `pyttsx3` |

---

## ❓ Troubleshooting

### 🔹 **Pyaudio Installation Error (Linux/Mac)**
If you face issues installing `pyaudio`, try:
```bash
pip install pyaudio
```
For Linux:
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### 🔹 **No Speech Recognition / Poor Accuracy**
- Ensure your **microphone is working** and set as the default input device.
- Try using a **better-quality microphone** for clearer input.

### 🔹 **Vosk Model Not Found**
Ensure the model is **downloaded and extracted** into the `model/` directory:
```
PronunciationTrainer/
├── ASD_Speech.py
├── model/
│   ├── vosk-model-small-en-us-0.15/
│   │   ├── files...
```

If missing, download again:
```bash
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip -d model
```

---

## 📜 License
This project is **open-source** and available under the **MIT License**.

---

## 🙌 Contributions
We welcome contributions! If you'd like to improve this project:
1. **Fork** this repository.
2. **Create** a new feature branch.
3. **Submit** a pull request.
