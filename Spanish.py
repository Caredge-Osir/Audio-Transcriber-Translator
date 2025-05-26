import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import os
import whisper

os.environ["PATH"] += os.pathsep + r"C:\Users\ombik\OneDrive\Desktop\Spanish\essentials_build\bin"

model = whisper.load_model("base")
result = model.transcribe(r"C:\Users\ombik\OneDrive\Desktop\Spanish\Audio\PISTA 001.mp3", language="es")

print("Spanish:", result["text"])

