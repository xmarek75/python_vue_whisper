# backend/utils.py
import whisper
from faster_whisper import WhisperModel
import json
import re
from datetime import datetime, timedelta
import logging

# Nastavení logování
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
def load_whisper(name):
    # Načtení modelu
    model = whisper.load_model("base")
    # Transkripce souboru
    result = model.transcribe(name)
    return result


def simple_hours(seconds: float) -> float:
    minutes = seconds // 60  # Celé minuty
    seconds = seconds % 60     # Zbytek sekund
    return minutes, seconds

# Výpis transkripce s časovými značkami

def use_whisper(name):
    result = load_whisper(name)
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

# Funkce pro převod času ve formátu [minuty:sekundy]
def convert_to_datetime(minutes, seconds):
    start_time = timedelta(minutes=minutes, seconds=seconds)
    base_time = datetime(2014, 1, 1)  # Tato hodnota je pro naše výpočty fiktivní
    return base_time + start_time

def text_to_json(text):
    logging.debug(f"Text to process: {text[:200]}")  # Print the first 200 characters for debugging
    # Odstranění všech <br> tagů
    #text = text.replace("<br>", "")
    # Regulární výraz pro extrahování časových intervalů a obsahu
    pattern = r"\[(\d+):(\d+) - (\d+):(\d+)\] (.*?)(?=\[|\Z)"

    # Výsledný seznam pro JSON
    result = []
    id_counter = 1

    # Iterace přes všechny shody
    for match in re.finditer(pattern, text):
        start_minute, start_second, end_minute, end_second, content = match.groups()

        # Zkontrolujte, co je v content, než ho přidáte do výsledného seznamu
        logging.debug(f"Match found: Start: {start_minute}:{start_second} End: {end_minute}:{end_second} Content: {content.strip()}")

        # Převod start a end času na datetime
        start_time = convert_to_datetime(int(start_minute), int(start_second))
        end_time = convert_to_datetime(int(end_minute), int(end_second))

        # Přidání záznamu do výsledného seznamu
        result.append({
            "id": id_counter,
            "content": content.strip(),
            "start": start_time.isoformat(),
            "end": end_time.isoformat()
        })

        # Zvýšení id pro každý nový blok
        id_counter += 1

    # Zavolání funkce pro uložení dat do souboru
    save_to_json(result)
    return result

def save_to_json(data):
    file_path = "../vue_folder/public/data.json"
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logging.info("Data byla úspěšně uložena do souboru.")
    except Exception as e:
        logging.error(f"Chyba při zápisu do souboru: {e}")

def save_text_to_file(file_path: str, json_text: str):
    """
    Uloží text do JSON souboru na dané cestě. Přepíše soubor novým obsahem.
    """
    try:
        # Validace JSON formátu
        json_data = json.loads(json_text)

        # Zajištění, že data mají správný formát (pole objektů)
        if not isinstance(json_data, list) or not all(isinstance(item, dict) for item in json_data):
            raise ValueError("JSON musí být pole objektů.")

        # Zapsání do souboru
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(json_data, file, ensure_ascii=False, indent=2)

        logger.info(f"Data úspěšně uložena do {file_path}.")
    except json.JSONDecodeError as e:
        logger.error(f"Neplatný JSON formát: {e}")
        raise ValueError("Neplatný JSON formát.") from e
    except Exception as e:
        logger.error(f"Chyba při ukládání do {file_path}: {e}")
        raise Exception(f"Chyba při ukládání do souboru: {e}")

# Funkce pro testování
def test_text_processing():
    input_text = """[0:0 - 0:5]  What is she doing in the kitchen?
[0:5 - 0:9]  Cooking dinner. She is cooking dinner.
[0:9 - 0:12]  Is she washing dishes?
[0:12 - 0:16]  No, she isn't. She is not washing dishes.
[0:16 - 0:21]  She is cooking the meal. Cooking the dinner.
[0:21 - 0:25]  Is she cooking dinner in the garage?
[0:25 - 0:28]  No, she is not in the garage.
[0:28 - 0:31]  She is cooking the dinner in the kitchen.
[0:31 - 0:34]  If you want to complete your practice of this story,
[0:34 - 0:37]  you can go to EnglishEasyPractice.com
[0:37 - 0:40]  and download the audio lessons of the story.
[0:40 - 0:44]  So you can practice English with it whenever and wherever you want.
[0:44 - 0:49]  Just listen to our short stories and answer the easy question out loud.
[0:49 - 0:53]  You will improve your listening and speaking skills fast.
[0:53 - 0:58]  And that's all for now. See you at EnglishEasyPractice.com."""

    text_to_json(input_text)

# Testování funkce
test_text_processing()

