import os
import whisper
from pytube import YouTube
from moviepy.editor import AudioFileClip, VideoFileClip
from deep_translator import GoogleTranslator

def download_video(video_url, filename="downloaded_video.mp4"):
    yt = YouTube(video_url)
    stream = yt.streams.filter(file_extension='mp4', only_video=False).first()
    stream.download(filename=filename)
    return filename

def extract_audio(video_path, audio_path="audio.wav"):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    return audio_path

def transcribe_audio(audio_path, language="es"):
    model = whisper.load_model("base")  # or "small", "medium", "large"
    result = model.transcribe(audio_path, language=language)
    return result["text"]

def translate_text(text, source_lang="es", target_lang="en"):
    translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
    return translated

def process_video(video_url):
    print("[1] Downloading video...")
    video_file = download_video(video_url)

    print("[2] Extracting audio...")
    audio_file = extract_audio(video_file)

    print("[3] Transcribing audio...")
    spanish_text = transcribe_audio(audio_file)
    print(f"Transcribed (Spanish):\n{spanish_text}\n")

    print("[4] Translating text...")
    english_text = translate_text(spanish_text)
    print(f"Translated (English):\n{english_text}\n")

    return spanish_text, english_text

# Example usage:
video_link = "https://www.youtube.com/watch?v=EXAMPLE_ID"  # Replace with actual link
spanish_text, english_text = process_video(video_link)
