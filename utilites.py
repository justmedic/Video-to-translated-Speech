import os
import os
from pytube import YouTube
from moviepy.editor import AudioFileClip

def ffmpeg_append():
    """
    Добавляет ffmpeg (утилиту для работы с аудио) в PATH локально
    """
    # Путь к папке с ffmpeg в вашем проекте
    ffmpeg_path = '......\\ffmpeg\\bin'

    os.environ["PATH"] += os.pathsep + ffmpeg_path


def download_audio(url: str, user_filename: str):
    """Скачать только аудиопоток YouTube-видео и сохранить в файл."""
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.get_audio_only()
        audio_stream.download(filename=user_filename)
        print('Аудио скачано успешно.')
    except Exception as e:
        print(f"Произошла ошибка при скачивании аудио: {e}")

def convert_to_wav(file_name: str):
    """Конвертировать аудиофайл в формат WAV."""
    try:
        audio_clip = AudioFileClip(file_name)
        audio_clip.write_audiofile("audio.wav")
        print('Аудио конвертировано в формат WAV и сохранено.')
    except Exception as e:
        print(f"Произошла ошибка при конвертации в WAV: {e}")

def get_video_duration(url: str) -> float:
    """Получить длительность видео с YouTube."""
    try:
        yt = YouTube(url)
        duration = yt.length  # Длительность возвращается в виде целого числа (секунды)
        return float(duration)
    except Exception as e:
        print(f"Ошибка при получении информации о длительности видео: {e}")
        return 0.0

def delete_file(file_path: str):
    """Удалить файл, если он существует."""
    try:
        os.remove(file_path)
        print(f"Файл {file_path} успешно удален.")
    except OSError as e:
        print(f"Ошибка при удалении файла {file_path}: {e}")
