from PIL.Image import Image
from django.http import HttpRequest, HttpResponseNotFound, JsonResponse, HttpResponseNotAllowed
from numpy import asarray

from recognition.controllers.knn import predict


# from recognition.helpers import isValidType


def recognition(request: HttpRequest):
    if request.method == 'POST':

        if not request.FILES.get('foto'):
            return HttpResponseNotFound()

        foto = request.FILES['foto']

        # if not isValidType(foto.name):
        #     return JsonResponse({'erro': 'Foto inválida'}, status=422)

        foto = Image.open(foto)
        foto.load()

        if foto.mode == 'RGBA':
            foto_temp = Image.new('RGB', foto.size, (255, 255, 255))
            foto_temp.paste(foto, mask=foto.split()[3])
            foto = foto_temp

        resultado = predict(asarray(foto))

        if len(resultado) == 0:
            return JsonResponse({'erro': 'Nenhum rosto detectado'}, status=404)

        return JsonResponse({'cpf': resultado[0][0]})

    return HttpResponseNotAllowed(permitted_methods=['POST'])
