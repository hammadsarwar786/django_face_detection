import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from scipy.spatial.distance import cosine
import numpy as np
import cv2 as cv2
import mtcnn
from keras.models import load_model
from .utils import get_face, get_encode, load_pickle, l2_normalizer
import base64
from PIL import Image
import io
import os

current_path = os.path.abspath(__file__)
app_directory = os.path.dirname(current_path)

encoder_model = os.path.join(app_directory, 'data', 'model', 'facenet_keras.h5')
encodings_path = os.path.join(app_directory, 'data', 'encodings', 'encodings.pkl')

recognition_t = 0.35
required_size = (160, 160)

encoding_dict = load_pickle(encodings_path)
face_detector = mtcnn.MTCNN()
face_encoder = load_model(encoder_model)

@csrf_exempt
def post_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_to_detect = data.get('data')
            name, img, time,  = detect_face(image_to_detect)
            return JsonResponse({"name": name, "img": img, "time": time}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON format'}, status=400)

    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)




def detect_face(base64img):
    try:


        fetched_image = preprocess_image(base64img)
        image_array = np.array(fetched_image)

        img_rgb = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
        results = face_detector.detect_faces(img_rgb)

        # respone
        rep_name = ""
        rep_dist = ""

        for res in results:
            face, pt_1, pt_2 = get_face(img_rgb, res['box'])
            encode = get_encode(face_encoder, face, required_size)
            encode = l2_normalizer.transform(np.expand_dims(encode, axis=0))[0]
            name = 'unknown'
            distance = float("inf")

            for db_name, db_encode in encoding_dict.items():
                dist = cosine(db_encode, encode)
                if dist < recognition_t and dist < distance:
                    name = db_name
                    distance = dist
            if name == 'unknown':
                cv2.rectangle(img_rgb, pt_1, pt_2, (0, 0, 255), 6)
                cv2.putText(img_rgb, "", (pt_1[0], pt_1[1] + 20), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                rep_name = name
                rep_dist = distance

            else:
                cv2.rectangle(img_rgb, pt_1, pt_2, (0, 255, 0), 20)
                cv2.putText(img_rgb, name.split(".")[0], (pt_1[0], pt_1[1] + 20), cv2.FONT_HERSHEY_SIMPLEX, 3,
                            (0, 255, 0), 2)
                rep_name = name
                rep_dist = distance

        # cv2.imwrite(test_res_path, img_rgb)
        # Convert the image array to bytes
        image_bytes = cv2.imencode('.jpg', img_rgb)[1].tobytes()
        # Encode the image bytes to base64
        base64_data = base64.b64encode(image_bytes)
        # Convert the base64 data to a string
        base64_string = base64_data.decode("utf-8")
        return rep_name, base64_string, str(rep_dist)
    except:
        return JsonResponse({'message': 'Invalid face format'}, status=400)

def preprocess_image(image_data):
    encoded = image_data
    image_bytes = base64.b64decode(encoded)
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    return image

