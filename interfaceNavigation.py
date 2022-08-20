import os
import pyautogui
import json
from components import textParser, switchTab
from google.cloud.vision_v1 import AnnotateImageResponse

credential_path = "C:/Users/ANDRE/Quarantine/Frontfacing_Python_Projects/MTGO_Computer_Vision_V2/assets/credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
# run in Powershell
# set GOOGLE_APPLICATION_CREDENTIALS=C:\Users\ANDRE\Quarantine\Frontfacing_Python_Projects\MTGO_Computer_Vision_V2\assets\credentials.json
# image = pyautogui.screenshot('./assets/liveScreenshot.png')
response = textParser('./assets/resultScreen.png')
serializedResponse = AnnotateImageResponse.to_json(response)
with open("./assets/screenshotText.txt", "w") as file:
    file.write(json.dumps(serializedResponse))

with open("./assets/screenshotText.txt", "r") as file:
    file = json.load(file)
response = json.loads(file)
entries = response["textAnnotations"][1:]
texts = [entry["description"] for entry in entries]
locations = [entry["boundingPoly"]["vertices"] for entry in entries]

records = [entry for entry in entries if len(entry["description"]) == 3 and entry["description"][0].isdigit() and
           entry["description"][1] == "-" and entry["description"][2].isdigit()]
gameColumns = [entry for entry in entries if entry["description"] == "Games"]
gameColumnWidths = []
for gameColumn in gameColumns:
    minX = min([vertex["x"] for vertex in gameColumn["boundingPoly"]["vertices"]])
    maxX = max([vertex["x"] for vertex in gameColumn["boundingPoly"]["vertices"]])
    gameColumnWidths.append([minX, maxX])

for record in records:
    vertices = record["boundingPoly"]["vertices"]
    averageX = sum([vertex["x"] for vertex in vertices]) / 4
    averageY = sum([vertex["y"] for vertex in vertices]) / 4
    record["Location"] = [averageX, averageY]

switchTab()

for record in records:
    # print(record["Location"])
    if any(record["Location"][0] in range(minX, maxX) for minX, maxX in gameColumnWidths):
        print(record["Location"])
        pyautogui.moveTo(record["Location"][0], record["Location"][1], duration=0.3)

# print(actualRecords)
