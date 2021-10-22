import mimetypes
from typing import Union

import face_recognition
import numpy as np
from PIL import Image


def image_extension(content_type: str) -> Union[str, None]:
    if content_type not in ['image/jpeg', 'image/png']:
        return None

    return mimetypes.guess_extension(content_type)


def has_valid_face(image: Image.Image) -> bool:
    # image = image.convert('RGB')
    width, height = image.size

    if width > 450 or height > 450:
        ratio = width / height
        new_size = (int(450 * ratio), 450)
        image = image.resize(new_size)

    image = np.array(image)

    face_bounding_boxes = face_recognition.face_locations(image)

    return not len(face_bounding_boxes) != 1


def image2gray(image: Image.Image):
    return image.convert(mode='L')


def rgba2rgb(image: Image.Image):
    new_image = Image.new('RGB', image.size, (255, 255, 255))
    new_image.paste(image, mask=image.getchannel('A'))

    return new_image
