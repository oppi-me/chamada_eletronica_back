from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from recognition.add_face import add_face
from recognition.recognition_face import recognition_face
from . import utils
from .models import Client, Student


@csrf_exempt
@require_POST
def ping(request: HttpRequest):
    ip = utils.get_ip(request)
    mac_address = utils.get_mac_address(request)

    if not utils.is_valid_mac_address(mac_address):
        return HttpResponseBadRequest()

    try:
        client = Client.objects.get(mac_address=mac_address)
        client.ip = ip
        client.save()
    except Client.DoesNotExist:
        Client.objects.create(mac_address=mac_address, ip=ip)

    return HttpResponse()


@csrf_exempt
@require_POST
def recognition(request: HttpRequest):
    image_data = request.read()
    mac_address = utils.get_mac_address(request)

    try:
        results = recognition_face(image_data)

        if len(results) != 1:
            raise Exception('Nenhum ou mais de um resultado encontrado.')

        client = Client.objects.get(mac_address=mac_address)
        student = Student.objects.get(cpf=results[0][0])

        __make_entry(client, student)

    except (Client.DoesNotExist, Student.DoesNotExist):
        return JsonResponse({'erro': 'MAC ou identificador não encontrado no banco de dados.'}, status=422)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=422)

    return JsonResponse({
        'class': student.c_lass,
        'enrolment': student.enrolment,
        'name': student.name,
        'shift': student.shift
    })


@csrf_exempt
@require_POST
def register(request: HttpRequest):
    image_data = request.read()
    mac_address = utils.get_mac_address(request)

    try:
        client = Client.objects.get(mac_address=mac_address)

        if not client.registering or request.content_type is None:
            return HttpResponse()

        add_face(client.registering, image_data, request.content_type)

    except Client.DoesNotExist:
        return JsonResponse({'erro': 'Totem não encontrado no banco de dados.'}, status=403)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=422)

    return HttpResponse()


def __make_entry(client, student):
    pass
