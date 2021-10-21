import filecmp
import io
import os
import uuid
from typing import Union

import face_recognition
import numpy as np
from PIL import Image, UnidentifiedImageError
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from chamada_eletronica.settings import BASE_DIR
from helpers import cpf as CPF
from recognition.helpers import image_extension


@csrf_exempt
def add(request: HttpRequest):
    if request.method == 'POST':
        cpf = request.GET.get('cpf', default=None)
        image_data = request.read()

        if cpf is None or image_data == b'':
            return HttpResponse(status=422)

        extension = image_extension(request.content_type)

        if not CPF.isValid(cpf) or extension is None:
            return JsonResponse({'erro': 'CPF ou formato de imagem inválido'}, status=422)

        result = __save_image(image_data, extension, cpf)

        if isinstance(result, str):
            return JsonResponse({'erro': result}, status=422)

        return HttpResponse()

    return HttpResponseNotAllowed(permitted_methods=['POST'])


def __save_image(image_data: bytes, ext: str, cpf: str) -> Union[str, bool]:
    try:
        image: Image.Image = Image.open(io.BytesIO(image_data))
    except UnidentifiedImageError:
        return 'Formato inválido.'

    directory = os.path.join(BASE_DIR, 'static', cpf)

    if not os.path.exists(directory):
        os.makedirs(directory)

    images_in_dir = os.listdir(directory)

    name = str(len(images_in_dir) + 1) + ext
    definitive_image_path = os.path.join(directory, name)

    if not hasValidFace(image):
        return 'Nenhum ou mais de um rosto foi encontrado na image.'

    if len(images_in_dir) > 0:
        temp_name = 'temp-' + str(uuid.uuid4().hex) + ext
        temp_image_path = os.path.join(directory, temp_name)

        image.save(temp_image_path)

        for image_in_dir in images_in_dir:
            image_to_compare_path = os.path.join(directory, image_in_dir)

            if filecmp.cmp(temp_image_path, image_to_compare_path, shallow=False):
                os.remove(temp_image_path)
                return 'Imagem repetida.'

        os.rename(temp_image_path, definitive_image_path)

    else:
        image.save(definitive_image_path)

    return True


def hasValidFace(image: Image.Image) -> bool:
    # image = image.convert('RGB')
    width, height = image.size

    if width > 450 or height > 450:
        ratio = width / height
        new_size = (int(450 * ratio), 450)
        image = image.resize(new_size)

    image = np.array(image)

    face_bounding_boxes = face_recognition.face_locations(image)

    return not len(face_bounding_boxes) != 1
