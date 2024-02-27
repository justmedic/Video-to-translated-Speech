import os
import torch
from pydub import AudioSegment
import librosa
import soundfile as sf
from transliterate import translit
import re
from librosa import get_duration
from utilites import ffmpeg_append
import wave


ffmpeg_append()  # добавление утилиты


class SoundSynthesis:
    def __init__(self, model_path='model.pt', model_url='https://models.silero.ai/models/tts/ru/v4_ru.pt'):
        """
        Конструктор класса SoundSynthesis для инициализации и загрузки модели Text-to-Speech.

        :param model_path: Путь к файлу модели для загрузки; если файла нет, он будет загружен.
        :param model_url: URL для загрузки модели, если файл отсутствует локально.
        """
        self.device = torch.device('cpu')
        torch.set_num_threads(4)

        
        if not os.path.isfile(model_path):#для загрузки модели если не установлена
            torch.hub.download_url_to_file(model_url, model_path)
        
        self.model = torch.package.PackageImporter(model_path).load_pickle("tts_models", "model")
        self.model.to(self.device)
        self.sample_rate = 48000  # герцовка звука (хз на что влияет но лучше не трогать)

        self.files_to_remove = []

        self._english_word_pattern = re.compile(r'\b[a-zA-Z]+\b')

    def voiceover_conversion(self, text_list, voice_actor):
        """
        Обрабатывает список текстовых элементов для создания их аудиоверсии.
        Сначала транслитерирует слова на английском языке в русский транслит,
        затем использует текст для синтеза речи и создания WAV-файлов озвучки.
        После чего объединяет все аудиофайлы в один MP3-файл и очищает временные файлы.

        :param text_list: Список словарей, где каждый словарь содержит ключ 'text'
                          с текстом для озвучивания.
        :param len_original_sound: Продолжительность оригинального аудио, используется
                                   для добавления тишины в конец чтобы можно было накладывать озвучки друг на друга без рассинхрона.
        """
        try:
            for elements in text_list:
                elements['text'] = self._transliterate_english_words(elements['text'])

                if '%' in elements['text']:
                    elements['text'] = elements['text'].replace('%', 'процент') #заглушка, хз как пофиксить баг с процентов, потом разберусь

                filename = self._text_to_speech(elements['text'], speaker= voice_actor, filename = f"{str(elements['start'])}.wav")
                self._get_speed(filename, elements['start'], elements['end'])

            result_audio_name = self._concatenate_wav_to_mp3()#когда цикл завергил работу, то мы соединаем все чанки в единый файл озвучки
            print(f"result_vid_name = {result_audio_name}")
        except Exception as e:
            print(f"Чета пошло не так {e}")
        finally:
            self._cleanup_files()
        

        print('END')


    def _text_to_speech(self, text, speaker='eugene', filename='speech.wav'): #aidar, baya, kseniya, xenia, eugene, random - все модели на ru 
        """
        Преобразует текст в речь, сохраняет в файл и достигает нужной продолжительности аудиосегмента.

        :param text: Текст для преобразования.
        :param speaker: Исполнитель речи.
        :param filename: Имя файла для сохранения речи.
        :return: Путь к созданному аудио-файлу.
        """

        
        # Преобразуйте текст в речь и сохраните в файл
        audio_path = self.model.save_wav(text=text, speaker=speaker, sample_rate=self.sample_rate)
        
        #переименование для чанков
        os.rename(audio_path, filename)

        self.files_to_remove.append(filename)
        return filename

    def _concatenate_wav_to_mp3(self, output_wav = 'resuls.wav', output_mp3 = 'result.mp3' ):
        """
        Для объединения всех wav файлов и перевод финального файла в mp3 формат
        """
        wav_files = self.files_to_remove
        combined = AudioSegment.empty()

        for wav_file in wav_files:
            sound = AudioSegment.from_wav(wav_file)
            combined += sound
 
        combined.export(output_wav, format="wav")
        combined.export(output_mp3, format="mp3")
        os.remove(output_wav)
        return output_mp3
    
    def _cleanup_files(self):
        """
        Удаляет все временные файлы
        """
        for filepath in self.files_to_remove:
            try:
                os.remove(filepath)
            except OSError as e:
                print(f"Error: {filepath} : {e.strerror}")

    def _get_speed(self, filename:str, time_start:float, time_end:float):
        """
        Подгоняет продолжительность wav файлов (каждого чанка) под целевое значение
        """
        target_time = (time_end - time_start)
        real_time = get_duration(filename=filename)
        acceleration_factor = target_time / real_time

        print(f'filename = {filename}, target_time: {target_time}, real_time: {real_time}, acceleration_factor: {acceleration_factor}')

        TOLERANCE = 0.01  # 1% допуск, оптимизация? я хз зачем это но вроде нужная вещь
        if abs(1 - acceleration_factor) < TOLERANCE:
            print(f"Аудио '{filename}' уже в пределах целевого времени.")
            return real_time, target_time

        try:
            if acceleration_factor < 1:  # Ускорение речи
                print("Ускорение")
                audio, sample_rate = librosa.load(filename, sr=None)
                audio_stretched = librosa.effects.time_stretch(audio, rate=1/acceleration_factor)
                sf.write(filename, audio_stretched, sample_rate)
            else:  # Добавление тишины
                print('Добавление тишины')
                original_audio = AudioSegment.from_file(filename)
                silence_duration_ms = int((target_time - real_time) * 1000)
                print(f'silence_duration_ms: {silence_duration_ms}')
                silence = AudioSegment.silent(duration=silence_duration_ms // 2)
                audio_with_silence = silence + original_audio + silence
                audio_with_silence.export(filename, format="wav")
        except Exception as e:
            print(f"Произошла ошибка при обработке файла '{filename}': {e}")

        return real_time, target_time


    def _transliterate_english_words(self, text:str):
        """Транслитерирует английские слова в тексте."""
        words = text.split()
        

        transliterated_words = [
            translit(word, 'ru') if self._english_word_pattern.match(word) else word
            for word in words
        ]
        
        return ' '.join(transliterated_words)
    
    def _get_wav_length(self, wav_file_path):
        with wave.open(wav_file_path, 'r') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            return duration
        
