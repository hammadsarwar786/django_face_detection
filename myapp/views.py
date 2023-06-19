import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
import base64
from PIL import Image
import io
import face_recognition
import numpy as np


@csrf_exempt
def post_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_to_detect = data.get('data')
            #
            success, message, matched_image,face_dimension = find_matching_image(image_to_detect)
            return JsonResponse({"success": success, "message": message, "data": matched_image, "face": face_dimension}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)




def preprocess_image(image_data):
    #.split(",")[1]
    encoded = image_data
    image_bytes = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return image

def find_matching_image(image_data):
    image_to_detect = preprocess_image(image_data)
    face_to_detect = face_recognition.face_encodings(np.array(image_to_detect))[0]

    for root, dirs, files in os.walk(settings.STATIC_ROOT):
        for file in files:
            if file.endswith(".jpg") or file.endswith(".jpeg"):
                image_path = os.path.join(settings.STATIC_ROOT, "images/")
                face_image = face_recognition.load_image_file(image_path+ file)
                print(image_path)
                #get face
                face_location = face_recognition.face_locations(np.array(image_to_detect))[0]
                # new code
                face_locations = face_recognition.face_locations(face_image)  # Retrieve face bounding box coordinates
                face_encodings = face_recognition.face_encodings(face_image, face_locations)
                if len(face_encodings) > 0:
                    match = face_recognition.compare_faces([face_to_detect], face_encodings[0])
                    if match[0]:
                        return "true", "Authorized", file, face_location,
                    else:
                        return "false", "Un Authorized", "Unknwon", face_location,

    return "error", "error", "error", "error",
