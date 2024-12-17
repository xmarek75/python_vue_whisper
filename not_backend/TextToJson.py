import json
import re
from datetime import datetime, timedelta

# Původní text
text = """
[0:0 - 0:5] What is she doing in the kitchen?<br>
[0:5 - 0:9] Cooking dinner. She is cooking dinner.<br>
[0:9 - 0:12] Is she washing dishes?<br>
[0:12 - 0:16] No, she isn't. She is not washing dishes.<br>
[0:16 - 0:21] She is cooking the meal. Cooking the dinner.<br>
[0:21 - 0:25] Is she cooking dinner in the garage?<br>
[0:25 - 0:28] No, she is not in the garage.<br>
[0:28 - 0:31] She is cooking the dinner in the kitchen.<br>
[0:31 - 0:34] If you want to complete your practice of this story,<br>
[0:34 - 0:37] you can go to EnglishEasyPractice.com<br>
[0:37 - 0:40] and download the audio lessons of the story.<br>
[0:40 - 0:44] So you can practice English with it whenever and wherever you want.<br>
[0:44 - 0:49] Just listen to our short stories and answer the easy question out loud.<br>
[0:49 - 0:53] You will improve your listening and speaking skills fast.<br>
[0:53 - 0:58] And that's all for now. See you at EnglishEasyPractice.com.<br>
"""

# Funkce pro převod času ve formátu [minuty:sekundy]
def convert_to_datetime(minutes, seconds):
    start_time = timedelta(minutes=minutes, seconds=seconds)
    base_time = datetime(2014, 1, 1)  # Tato hodnota je pro naše výpočty fiktivní
    return base_time + start_time

# Regulární výraz pro extrahování časových intervalů a obsahu
pattern = r"\[(\d+):(\d+) - (\d+):(\d+)\] (.*?)<br>"

# Výsledný seznam pro JSON
result = []
id_counter = 1

# Iterace přes všechny shody
for match in re.finditer(pattern, text):
    start_minute, start_second, end_minute, end_second, content = match.groups()

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

# Výstup výsledného JSON
json_output = json.dumps(result, indent=2)
print(json_output)
