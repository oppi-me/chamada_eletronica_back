import filecmp
import os
import uuid

from chamada_eletronica.settings import BASE_DIR
from . import utils
from .errors import InvalidImageForTrainingError, RepeatedImageError


def add_face(id: str, image_data: bytes, content_type: str):
    extension = utils.image_extension(content_type)

    __save_image(image_data, extension, id)


def __save_image(image_data: bytes, ext: str, id: str) -> None:
    image = utils.binary2image(image_data)
    image = utils.image2gray(image)

    directory = os.path.join(BASE_DIR, 'static', id)

    if not os.path.exists(directory):
        os.makedirs(directory)

    images_in_dir = os.listdir(directory)

    name = str(len(images_in_dir) + 1) + ext
    definitive_image_path = os.path.join(directory, name)

    if utils.number_of_faces(image) != 1:
        raise InvalidImageForTrainingError

    if len(images_in_dir) > 0:
        temp_name = 'temp-' + str(uuid.uuid4().hex) + ext
        temp_image_path = os.path.join(directory, temp_name)

        image.save(temp_image_path)

        for image_in_dir in images_in_dir:
            image_to_compare_path = os.path.join(directory, image_in_dir)

            if filecmp.cmp(temp_image_path, image_to_compare_path, shallow=False):
                os.remove(temp_image_path)
                raise RepeatedImageError

        os.rename(temp_image_path, definitive_image_path)

    else:
        image.save(definitive_image_path)
