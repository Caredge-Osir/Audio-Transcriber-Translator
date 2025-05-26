import os
import whisper
import warnings

# Optional: Suppress FP16 CPU warning
warnings.filterwarnings("ignore", category=UserWarning)

# Set ffmpeg path manually if needed
os.environ["PATH"] += os.pathsep + r"C:\Users\ombik\OneDrive\Desktop\Spanish\essentials_build\bin"

# Load Whisper model
model = whisper.load_model("base")

# Folder containing all your audio files
audio_folder = r"C:\Users\ombik\OneDrive\Desktop\Spanish\Audio"

# Create an output folder for transcriptions (optional)
output_folder = os.path.join(audio_folder, "Transcripts")
os.makedirs(output_folder, exist_ok=True)

# Supported audio extensions
supported_exts = [".mp3", ".wav", ".m4a", ".flac", ".ogg"]

# Loop through all files in the folder
for filename in os.listdir(audio_folder):
    if any(filename.lower().endswith(ext) for ext in supported_exts):
        audio_path = os.path.join(audio_folder, filename)
        print(f"Transcribing: {filename}...")

        try:
            result = model.transcribe(audio_path, language="es")

            # Print to terminal
            print("Text:", result["text"])

            # Save to .txt file
            name_without_ext = os.path.splitext(filename)[0]
            output_path = os.path.join(output_folder, f"{name_without_ext}.txt")

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(result["text"])

        except Exception as e:
            print(f"Error with file {filename}: {e}")

print("\n✅ Transcription complete for all audio files.")

