from __future__ import print_function
import statistics
import time
import pyautogui
from google.cloud import vision
import os
import io
from PIL import Image, ImageDraw
from google.cloud.vision_v1 import AnnotateImageResponse
import json
from components import switchTab
import pytesseract
from navigation_components import download_atomic_cards, get_archetype_maps, collectGameText, processGameText
from difflib import SequenceMatcher

def draw_box(image, vertices, color):
    """Draw a border around the image using the hints in the vector list."""
    draw = ImageDraw.Draw(image)
    draw.polygon(
        [
            vertices[0]["x"],
            vertices[0]["y"],
            vertices[1]["x"],
            vertices[1]["y"],
            vertices[2]["x"],
            vertices[2]["y"],
            vertices[3]["x"],
            vertices[3]["y"],
        ],
        None,
        color,
    )
    return image

def checkJoin(inputEntry, inputEntries):
    for index, potentialEntry in enumerate(inputEntries):
        if abs(inputEntry["boundingPoly"]["vertices"][1]["x"] - potentialEntry["boundingPoly"]["vertices"][0]["x"]) < 3 \
                and inputEntry["boundingPoly"]["vertices"][1]["y"] == potentialEntry["boundingPoly"]["vertices"][0]["y"]:
            potentialEntry["description"] = inputEntry["description"] + potentialEntry["description"]
            potentialEntry["boundingPoly"]["vertices"][0] = inputEntry["boundingPoly"]["vertices"][0]
            potentialEntry["boundingPoly"]["vertices"][3] = inputEntry["boundingPoly"]["vertices"][3]
            inputEntries.pop(inputEntries.index(inputEntry))
            checkJoin(potentialEntry, inputEntries)
            return True
        elif abs(inputEntry["boundingPoly"]["vertices"][0]["x"] - potentialEntry["boundingPoly"]["vertices"][1]["x"]) < 3 \
            and inputEntry["boundingPoly"]["vertices"][1]["y"] == potentialEntry["boundingPoly"]["vertices"][0]["y"]:
            potentialEntry["description"] = potentialEntry["description"] + inputEntry["description"]
            potentialEntry["boundingPoly"]["vertices"][1] = inputEntry["boundingPoly"]["vertices"][1]
            potentialEntry["boundingPoly"]["vertices"][2] = inputEntry["boundingPoly"]["vertices"][2]
            inputEntries.pop(inputEntries.index(inputEntry))
            checkJoin(potentialEntry, inputEntries)
            return True
    return False

credential_path = "C:/Users/ANDRE/Quarantine/Frontfacing_Python_Projects/MTGO_Computer_Vision_V2/assets/credentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
switchTab()
time.sleep(2)
image = pyautogui.screenshot('./liveAssets/liveScreenshot.png')

with io.open('liveAssets/liveScreenshot.png', 'rb') as image_file:
    content = image_file.read()
image = vision.Image(content=content)
client = vision.ImageAnnotatorClient()
response = client.document_text_detection(image=image)
serializedResponse = AnnotateImageResponse.to_json(response)
serializedResponse = json.loads(serializedResponse)

entries = serializedResponse["textAnnotations"][1:]
entriesTemp = entries
for entry in entriesTemp:
    joining = checkJoin(entry, entries)
for entry in entries:
    vertices = entry["boundingPoly"]["vertices"]
    averageX = sum([vertex["x"] for vertex in vertices]) // 4
    averageY = sum([vertex["y"] for vertex in vertices]) // 4
    entry["Location"] = [averageX, averageY]
    entry["Height"] = [min([vertex["y"] for vertex in vertices]), max([vertex["y"] for vertex in vertices])]
    entry["Width"] = [min([vertex["x"] for vertex in vertices]), max([vertex["x"] for vertex in vertices])]


def filterEntries(entries, filter: str, sort=None):
    output = [entry for entry in entries if filter in entry["description"]]
    if sort:
        output = sorted(output, key=sort)
    if len(output) == 1:
        return output[0]
    else:
        return output

primaryNameColumn = filterEntries(entries, "Name")
primaryRankColumn = filterEntries(entries, "Rank")
primaryRecordColumn = filterEntries(entries, "Record")
matchOpponentColumns = filterEntries(entries, "Round", lambda x: x["Location"][0])
medianOpponentColumnY = statistics.median([opponentColumn["Location"][1] for opponentColumn in matchOpponentColumns])
matchOpponentColumns = [column for column in matchOpponentColumns if abs(column["Location"][1] - medianOpponentColumnY) <= 10]
matchResultColumns = filterEntries(entries, "Games", lambda x: x["Location"][0])


names = [entry for entry in entries if entry["Location"][0] in range(primaryNameColumn["Width"][0] - 15,
                    primaryNameColumn["Width"][1] + 15) and entry["Location"][1] > primaryNameColumn["Location"][1]]
ranks = [entry for entry in entries if entry["Location"][0] in range(primaryRankColumn["Width"][0] - 15,
                    primaryRankColumn["Width"][1] + 15) and entry["Location"][1] > primaryRankColumn["Location"][1]]
records = [entry for entry in entries if entry["Location"][0] in range(primaryRecordColumn["Width"][0] - 15,
                    primaryRecordColumn["Width"][1] + 15) and entry["Location"][1] > primaryRecordColumn["Location"][1]]
names = sorted(names, key=lambda x: x["Location"][1])
ranks = sorted(ranks, key=lambda x: x["Location"][1])
records = sorted(records, key=lambda x: x["Location"][1])

enter_replay_path = "navigation_assets/Enter Replay Button.png"
exit_replay_path = "navigation_assets/Exit Replay.png"
bottom_left_reference_path = "navigation_assets/Game Log Bottom Left Reference.png"
top_right_reference_path = "navigation_assets/Game Log Top Right Reference.png"
pytesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
maps = get_archetype_maps()
past_players = []
for name, rank, record in zip(names, ranks, records):
    opponentsPlayed = []
    recordsPlayed = []
    for entry in entries:
        if (entry["Location"][1] in range(name["Height"][0] - 10, name["Height"][1] + 10)) and any(entry["Location"][0] in range(matchOpponentColumn["Width"][0] - 15, matchOpponentColumn["Width"][1] + 15) for matchOpponentColumn in matchOpponentColumns):
            opponentsPlayed.append(entry)
        if (entry["Location"][1] in range(name["Height"][0] - 10, name["Height"][1] + 10)) and any(entry["Location"][0] in range(matchResultColumn["Width"][0] - 15, matchResultColumn["Width"][1] + 15) for matchResultColumn in matchResultColumns):
            recordsPlayed.append(entry)
    opponentsPlayed = sorted(opponentsPlayed, key=lambda x: x["Location"][0])
    recordsPlayed = sorted(recordsPlayed, key=lambda x: x["Location"][0])
    print("{} {} {} at location {}".format(rank["description"], name["description"], record["description"], name["Location"]))
    for index, opponent in enumerate(opponentsPlayed):
        if opponent["description"] == "(Bye)":
            recordsPlayed[index]["description"] = "0-0"
        for index, record in enumerate(recordsPlayed):
            if "-" not in record["description"]:
                recordsPlayed.pop(index)
    for opponent, record in zip(opponentsPlayed, recordsPlayed):
        if all(SequenceMatcher(None, name["description"], player_tuple[1]).ratio() < 0.8 or SequenceMatcher(None,
                            opponent["description"], player_tuple[0]).ratio() < 0.8 for player_tuple in past_players):
            past_players.append((name["description"], opponent["description"]))
            pyautogui.moveTo(record["Location"][0], record["Location"][1], duration=0.3)
            pyautogui.click()
            time.sleep(2)
            pyautogui.moveTo(enter_replay_path)
            pyautogui.click()
            while not pyautogui.locateCenterOnScreen(bottom_left_reference_path, confidence=.8) or not \
                    pyautogui.locateCenterOnScreen(top_right_reference_path, confidence=.8):
                pass
            game_text = collectGameText()
            processGameText(game_text, name["description"], opponent["description"], maps, record["description"])
            print("~~~~~~~~~~~~~~~~~~~~~")
            pyautogui.moveTo(exit_replay_path, duration=1)
            pyautogui.click()
    for opponentsPlayedEntry, recordsPlayedEntry in zip(opponentsPlayed, recordsPlayed):
        print("{} vs. {} at  opp location {} at record location {}".format(recordsPlayedEntry["description"], opponentsPlayedEntry["description"], recordsPlayedEntry["Location"], opponentsPlayedEntry["Location"]))
switchTab()
