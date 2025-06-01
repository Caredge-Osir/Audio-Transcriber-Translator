import os
import whisper
import warnings

# Suppress FP16 CPU warning
warnings.filterwarnings("ignore", category=UserWarning)

# Ensure ffmpeg path is included
os.environ["PATH"] += os.pathsep + r"C:\Users\ombik\OneDrive\Desktop\Spanish\essentials_build\bin"

# Load a more accurate Whisper model
model = whisper.load_model("small")  # Change to "medium" if your machine can handle it

# Folder containing your audio files
audio_folder = r"C:\Users\ombik\OneDrive\Desktop\Spanish\Audio"

# Combined output file for all transcripts
output_file = os.path.join(audio_folder, "All_Transcriptions.txt")

# List of supported audio formats
supported_exts = [".mp3", ".wav", ".m4a", ".flac", ".ogg"]

# Open the final transcript file
with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in sorted(os.listdir(audio_folder)):
        if any(filename.lower().endswith(ext) for ext in supported_exts):
            audio_path = os.path.join(audio_folder, filename)
            print(f"\n Transcribing: {filename}")

            try:
                # Transcribe with Spanish language and progress output
                result = model.transcribe(audio_path, language="es", verbose=True)

                # Write filename + transcription + two blank lines
                outfile.write(f"{filename}\n")
                outfile.write(result["text"].strip())
                outfile.write("\n\n\n")

            except Exception as e:
                print(f"Error with {filename}: {e}")

print("\n All transcriptions saved to:", output_file)
