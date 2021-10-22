import io
import os.path
import pickle

import face_recognition
import numpy as np
from PIL import Image, UnidentifiedImageError

from chamada_eletronica.settings import BASE_DIR
from .utils import image2gray


def face_recognition(image_data: bytes):
    try:
        image = Image.open(io.BytesIO(image_data))
    except UnidentifiedImageError:
        raise Exception('Formato inválido.')

    image = image2gray(image)

    results = __predict(np.asarray(image))

    return results if len(results) > 0 else None


def __predict(image,
              knn_clf=None,
              distance_threshold=0.5,
              model_path=os.path.join(BASE_DIR, 'static', 'trained_knn_model.clf')):
    if knn_clf is None and model_path is None:
        raise Exception("Um classificador ou modelo KNN deve ser fornecido.")

    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)
            print(knn_clf)

    x_face_locations = face_recognition.face_locations(image)

    if len(x_face_locations) == 0:
        return []

    faces_encodings = face_recognition.face_encodings(image, known_face_locations=x_face_locations)

    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)

    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(x_face_locations))]

    # Predict classes and remove classifications that aren't within the threshold
    return [[pred, loc] if rec else ["Desconhecido", loc] for pred, loc, rec in
            zip(knn_clf.predict(faces_encodings), x_face_locations, are_matches)]
