import os
import whisper
from deep_translator import GoogleTranslator
import warnings
import inflect
import re

# Suppress Whisper warning for FP16
warnings.filterwarnings("ignore", category=UserWarning)

# Set ffmpeg path manually (adjust as needed)
os.environ["PATH"] += os.pathsep + r"C:\Users\ombik\OneDrive\Desktop\Spanish\essentials_build\bin"

# Input/output settings
AUDIO_FOLDER = r"C:\Users\ombik\OneDrive\Desktop\Spanish\Audio"
OUTPUT_FILE = os.path.join(AUDIO_FOLDER, "Spanish-English.txt")

# Number-to-word engine
p = inflect.engine()

def convert_numbers_to_words(text):
    def replace(match):
        return p.number_to_words(match.group())
    return re.sub(r'\b\d+\b', replace, text)

def transcribe_audio(audio_path):
    try:
        print(f"  🔁 Loading Whisper model...")
        model = whisper.load_model("base")  # Change to "medium" or "large" for higher accuracy
        print(f"  🎙️ Transcribing...")
        result = model.transcribe(audio_path, language="es")
        text = result["text"].strip()
        return convert_numbers_to_words(text)
    except Exception as e:
        return f"[ERROR during transcription]: {str(e)}"

def translate_text(text):
    try:
        print(f"  🌐 Translating...")
        translated = GoogleTranslator(source="es", target="en").translate(text)
        return convert_numbers_to_words(translated)
    except Exception as e:
        return f"[ERROR during translation]: {str(e)}"

def process_all_audios(folder_path):
    print("🔍 Looking for audio files...")
    audio_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.mp3', '.wav', '.m4a'))])

    if not audio_files:
        print("❌ No audio files found in the folder.")
        return

    with open(OUTPUT_FILE, "w", encoding="utf-8") as output:
        for index, file in enumerate(audio_files, 1):
            print(f"\n🔊 [{index}/{len(audio_files)}] File: {file}")
            file_path = os.path.join(folder_path, file)

            # Transcribe
            spanish_text = transcribe_audio(file_path)
            print(f"  📝 Spanish:\n  {spanish_text}")

            # Translate
            english_text = translate_text(spanish_text)
            print(f"  ✅ English:\n  {english_text}")

            # Save output
            output.write(f"=== {file} ===\n")
            output.write("📝 Spanish:\n" + spanish_text + "\n\n")
            output.write("🌐 English:\n" + english_text + "\n")
            output.write("=" * 60 + "\n\n")

    print(f"\n✅ Done. Results saved to:\n📄 {OUTPUT_FILE}")

# Run the main processing function
process_all_audios(AUDIO_FOLDER)
