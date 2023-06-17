import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
from django.conf import settings
from PIL import Image
import base64
from PIL import Image
import io
import face_recognition
import numpy as np
import glob



###

# for root, dirs, files in os.walk(settings.STATIC_ROOT):
#     for file in files:
#         if file.endswith(".jpg"):
#             # image_list.append(file)
#             image_path = os.path.join(settings.STATIC_ROOT, "images\\")
#             image = Image.open(image_path + file)
#             image.show()
##

@csrf_exempt
def post_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_to_detect = data.get('data')
            matched_image = find_matching_image(image_to_detect)
            return JsonResponse({"response": matched_image}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)




def preprocess_image(image_data):
    encoded = image_data.split(",")[1]
    image_bytes = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return image

def find_matching_image(image_data):
    image_to_detect = preprocess_image(image_data)
    face_to_detect = face_recognition.face_encodings(np.array(image_to_detect))[0]

    for root, dirs, files in os.walk(settings.STATIC_ROOT):
        for file in files:
            if file.endswith(".jpeg"):
                image_path = os.path.join(settings.STATIC_ROOT, "images/")
                face_image = face_recognition.load_image_file(image_path+ file)
                # new code
                face_locations = face_recognition.face_locations(face_image)  # Retrieve face bounding box coordinates
                face_encodings = face_recognition.face_encodings(face_image, face_locations)
                if len(face_encodings) > 0:
                    match = face_recognition.compare_faces([face_to_detect], face_encodings[0])
                    if match[0]:
                        return file, face_locations[0],

    # for image_path in image_list:
    #     if image_path.lower().endswith(('.jpg', '.jpeg')):
    #         face_image = face_recognition.load_image_file(image_path)
    #         face_encodings = face_recognition.face_encodings(face_image)
    #         if len(face_encodings) > 0:
    #             match = face_recognition.compare_faces([face_to_detect], face_encodings[0])
    #             if match[0]:
    #                 return image_path

    return None

# def detect_face():
#     if 'imageToDetect' not in request.json:
#         return jsonify({'error': 'No imageToDetect parameter provided'}), 400

#     image_to_detect = request.json['imageToDetect']
#     matched_image = find_matching_image(image_to_detect)

#     if matched_image:
#         return jsonify({'matchedImage': matched_image}), 200
#     else:
#         return jsonify({'message': 'Image not found'}), 404
