import filecmp
import io
import os
import uuid

from PIL import Image, UnidentifiedImageError

from chamada_eletronica.settings import BASE_DIR
from .utils import image_extension, has_valid_face, image2gray


def add_face(id: str, image_data: bytes, content_type: str):
    if image_data == b'':
        raise Exception('Imagem vazia.')

    extension = image_extension(content_type)

    if extension is None:
        raise Exception('Extensão de imagem não aceita.')

    __save_image(image_data, extension, id)


def __save_image(image_data: bytes, ext: str, id: str) -> None:
    try:
        image: Image.Image = Image.open(io.BytesIO(image_data))
    except UnidentifiedImageError:
        raise Exception('Formato inválido.')

    image = image2gray(image)

    directory = os.path.join(BASE_DIR, 'static', id)

    if not os.path.exists(directory):
        os.makedirs(directory)

    images_in_dir = os.listdir(directory)

    name = str(len(images_in_dir) + 1) + ext
    definitive_image_path = os.path.join(directory, name)

    if not has_valid_face(image):
        raise Exception('Nenhum ou mais de um rosto foi encontrado na imagem.')

    if len(images_in_dir) > 0:
        temp_name = 'temp-' + str(uuid.uuid4().hex) + ext
        temp_image_path = os.path.join(directory, temp_name)

        image.save(temp_image_path)

        for image_in_dir in images_in_dir:
            image_to_compare_path = os.path.join(directory, image_in_dir)

            if filecmp.cmp(temp_image_path, image_to_compare_path, shallow=False):
                os.remove(temp_image_path)
                raise Exception('Imagem repetida.')

        os.rename(temp_image_path, definitive_image_path)

    else:
        image.save(definitive_image_path)
