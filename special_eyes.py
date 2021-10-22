import requests
from PIL import Image, ImageDraw
import math
post_url = "https://northcentralus.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceId=true&returnFaceLandmarks=true&recognitionModel=recognition_04&returnRecognitionModel=false&detectionModel=detection_03&faceIdTimeToLive=86400"

key_header = "Ocp-Apim-Subscription-Key"

source_image = "cad-20080602-358b1.x29067.jpg"
img_bytes = open(source_image, "rb").read()

headers = { key_header: key, "content-type": "application/octet-stream"}
req = requests.post(post_url, headers=headers, data=img_bytes)

result = req.json()

img = Image.open(source_image)

print(result)
def get_eye_bounding(landmarks, which):
    #eye_width = abs(landmarks[f"eyebrow{which}Inner"]["x"] - landmarks[f"eyebrow{which}Outer"]["x"])
    #eye_height = abs(landmarks[f"eye{which}Bottom"]["y"] - landmarks[f"eyebrow{which}Outer"]["y"])
    eye_width = abs(landmarks[f"eye{which}Inner"]["x"] - landmarks[f"eye{which}Outer"]["x"])
    eye_height = abs(landmarks[f"eye{which}Bottom"]["y"] - landmarks[f"eye{which}Top"]["y"])
    print(f"{which} eye width, height: {eye_width},{eye_height}")
    eye_diameter = max(eye_width, eye_height) * 1.75
    top_left = (landmarks[f"pupil{which}"]["x"] - eye_diameter /2, landmarks[f"pupil{which}"]["y"] - eye_diameter /2)
    bottom_right = (landmarks[f"pupil{which}"]["x"] + eye_diameter /2, landmarks[f"pupil{which}"]["y"] + eye_diameter /2)

    return [top_left, bottom_right]

def draw_eye(draw, which, landmarks,draw_bounding=True):
    eye =get_eye_bounding(landmarks, which)

    height = eye[1][1] - eye[0][1]
    pupil_diameter = height * 0.4

    pupil_center = [eye[1][0] - pupil_diameter - (pupil_diameter /4), eye[1][1] - pupil_diameter/2]
    
    draw.ellipse(eye, fill=(255,255,255))
    if draw_bounding:
        draw.rectangle(eye, outline=(255,0,0))
    draw.ellipse([
        pupil_center[0] - pupil_diameter/2,
        pupil_center[1] - pupil_diameter/2,
        pupil_center[0] + pupil_diameter/2,
        pupil_center[1] + pupil_diameter/2,
        ], fill=(0,0,0))

for face in result:
    face_rectangle = face["faceRectangle"]
    landmarks = face["faceLandmarks"]
    print(result)
    draw = ImageDraw.Draw(img)


    draw_eye(draw,"Left", landmarks, draw_bounding=False)
    draw_eye(draw,"Right", landmarks, draw_bounding=False)

img.save("test.jpg")