import tkinter as tk
from speach import SoundSynthesis
from translate import Translate
from recognize import recognize_speech_whisper
from gui import TranslationApp
from utilites import (ffmpeg_append, download_audio, convert_to_wav,
                      delete_file, get_video_duration)

ffmpeg_append()

def prog_logic(voice_actor, url):
    file_base = 'filename'
    speech_synthesizer = SoundSynthesis()
    
    try:
        download_audio(url, f'{file_base}.mp3')
        convert_to_wav(f'{file_base}.mp3')
        delete_file(f'{file_base}.mp3')

        print('Запуск распознавания речи...')
        audio_file_path = 'audio.wav'
        transcription = recognize_speech_whisper(audio_file_path)
    
        print('Распознавание завершено. Начинаем перевод...')
    
        translator = Translate("en", "ru")
        for element in transcription:
            element['text'] = translator.translate(element['text'])
        
        print(transcription)
    
    except Exception as e:
        print('Произошла ошибка:', e)
        return

    print('Перевод завершен. Начинаем синтез речи...')

    delete_file(audio_file_path)
  
    try:
        transcription[-1]['end'] = get_video_duration(url)
        speech_synthesizer.voiceover_conversion(transcription, voice_actor)
        print('Синтезация аудио завершена.')
    except IndexError:
        print('Ошибка: Транскрипция не содержит элементов.')


def main():
    """Основная функция: координация скачивания, конвертации, распознавания и синтеза речи."""
    
    root = tk.Tk()
    app = TranslationApp(root, prog_logic)
    root.mainloop()

if __name__ == '__main__':  
    main()
