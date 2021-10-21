import filecmp
import io
import os
import uuid

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
            return JsonResponse({'erro': 'CPF ou Imagem inválida'}, status=422)

        if __save_image(image_data, extension, cpf):
            return JsonResponse({'mensagem': 'Adicionado com Sucesso'})

        return JsonResponse({'mensagem': 'Imagem inválida ou repetida'})

    return HttpResponseNotAllowed(permitted_methods=['POST'])


def __save_image(image_data: bytes, ext: str, cpf: str) -> bool:
    try:
        image: Image.Image = Image.open(io.BytesIO(image_data))
    except UnidentifiedImageError:
        return False

    directory = os.path.join(BASE_DIR, 'static', cpf)

    if not os.path.exists(directory):
        os.makedirs(directory)

    images_in_dir = os.listdir(directory)

    name = str(len(images_in_dir) + 1) + ext
    definitive_image_path = os.path.join(directory, name)

    if len(images_in_dir) > 0:
        temp_name = 'temp-' + str(uuid.uuid4().hex) + ext
        temp_image_path = os.path.join(directory, temp_name)

        image.save(temp_image_path)

        for image_in_dir in images_in_dir:
            image_to_compare_path = os.path.join(directory, image_in_dir)

            if filecmp.cmp(temp_image_path, image_to_compare_path, shallow=False):
                os.remove(temp_image_path)
                return False

        os.rename(temp_image_path, definitive_image_path)

    else:
        image.save(definitive_image_path)

    return True
