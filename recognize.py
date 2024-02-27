"""
НИЧЕ НЕ ТРОГАТЬ ТУТ ВСЕ РАБОТАЕТ
"""
import whisper


def recognize_speech_whisper(audio_file_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file_path)
    segments = []
    for segment in result["segments"]:
            segments.append({
                "text": segment["text"],
                "start": segment["start"],
                "end": segment["end"],
            })

    for i in range(len(segments)-1):
        if segments[i]['end']!=segments[i+1]['start']:
            segments[i+1]['start'] = segments[i]['end']
        if "%" in segments[i]['text']:
             segments[i]['text'].replace('%', 'percent')

    return segments