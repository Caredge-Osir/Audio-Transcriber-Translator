import os
import whisper
import warnings
import inflect
import re
from deep_translator import GoogleTranslator

# Suppress Whisper FP16 warning
warnings.filterwarnings("ignore", category=UserWarning)

# Add ffmpeg to PATH
os.environ["PATH"] += os.pathsep + r"C:\Users\ombik\OneDrive\Desktop\Spanish\essentials_build\bin"

# Load Whisper model
model = whisper.load_model("medium")  # Use "large" if resources allow

# Define paths
audio_folder = r"C:\Users\ombik\OneDrive\Desktop\Spanish\Audio"
output_folder = os.path.join(audio_folder, "Transcripts")
os.makedirs(output_folder, exist_ok=True)

# Number-to-word conversion engine
p = inflect.engine()

# Supported file types
supported_exts = [".mp3", ".wav", ".m4a", ".flac", ".ogg"]

def convert_numbers_to_words(text):
    return re.sub(r'\b\d+\b', lambda m: p.number_to_words(m.group()), text)

def translate_to_english(text):
    try:
        translated = GoogleTranslator(source="es", target="en").translate(text)
        return convert_numbers_to_words(translated)
    except Exception as e:
        return f"[Translation Error] {e}"

# Begin processing audio files
for filename in sorted(os.listdir(audio_folder)):
    if any(filename.lower().endswith(ext) for ext in supported_exts):
        audio_path = os.path.join(audio_folder, filename)
        print(f"\n🎧 Processing: {filename}")

        try:
            # 1. Transcription
            result = model.transcribe(audio_path, language="es")
            spanish_raw = result["text"].strip()
            spanish_cleaned = convert_numbers_to_words(spanish_raw)

            # 2. Translation
            english_translated = translate_to_english(spanish_cleaned)

            # 3. Display on terminal
            print("\n📝 Transcripción (Español):\n" + spanish_cleaned)
            print("\n🌐 Translation (English):\n" + english_translated)

            # 4. Save to file
            base_name = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{base_name}.txt")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(f"=== {filename} ===\n\n")
                f.write("📝 Transcripción en Español:\n")
                f.write(spanish_cleaned + "\n\n")
                f.write("🌐 Traducción al Inglés:\n")
                f.write(english_translated + "\n")

            print(f"✅ Saved transcript: {output_path}")

        except Exception as e:
            print(f"❌ Error with file {filename}: {e}")
