import os
import pyautogui
import time
#
# credential_path = "C:/Users/ANDRE/Quarantine/Frontfacing_Python_Projects/MTGO_Computer_Vision_V2/assets/credentials.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
def textParser(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response
    return texts
    # texts = response.text_annotations
    # print('Texts:')
    #
    # for text in texts:
    #     print('\n"{}"'.format(text.description))
    #
    #     vertices = (['({},{})'.format(vertex.x, vertex.y)
    #                 for vertex in text.bounding_poly.vertices])
    #
    #     print('bounds: {}'.format(','.join(vertices)))
    #
    # if response.error.message:
    #     raise Exception(
    #         '{}\nFor more info on error messages, check: '
    #         'https://cloud.google.com/apis/design/errors'.format(
    #             response.error.message))

def documentTextParser(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    texts = response
    return texts

def switchTab():
    pyautogui.keyDown('alt')
    time.sleep(.2)
    pyautogui.press('tab')
    time.sleep(.2)
    pyautogui.keyUp('alt')

# detect_text("./assets/resultScreen.png")
