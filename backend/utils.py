# backend/utils.py
import whisper


def load_whisper():
    # Načtení modelu
    model = whisper.load_model("base")
    # Transkripce souboru
    result = model.transcribe("video_sample.mp4")
    return result


def simple_hours(seconds: float) -> float:
    minutes = seconds // 60  # Celé minuty
    seconds = seconds % 60     # Zbytek sekund
    return minutes, seconds

# Výpis transkripce s časovými značkami

def use_whisper():
    result = load_whisper()
    text_result = ''
    for segment in result["segments"]:
        start_time = segment["start"]  # Čas začátku segmentu
        end_time = segment["end"]      # Čas konce segmentu
        text = segment["text"]         # Text segmentu
        start_minutes, start_seconds = simple_hours(start_time)#prepis na minuty a vteriny
        end_minutes, end_seconds = simple_hours(end_time)

        new_string = f"[{start_minutes:.0f}:{start_seconds:.0f} - {end_minutes:.0f}:{end_seconds:.0f}] {text}"
        text_result = text_result +'\n'+ new_string

    return text_result

