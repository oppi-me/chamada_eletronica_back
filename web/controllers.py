from django.db import IntegrityError
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from recognition.add_face import add_face
from recognition.recognition_face import recognition_face
from . import utils
from .models import Client, Student


@csrf_exempt
@require_POST
def ping(request: HttpRequest):
    mac_address = request.POST.get('mac_address', default=None)

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    if mac_address is None or not utils.is_valid_mac_address(mac_address):
        return HttpResponseBadRequest()

    mac_address = utils.normalize_mac_address(mac_address)

    try:
        Client.objects.create(mac_address=mac_address, ip=ip)
    except IntegrityError:
        pass

    try:
        client = Client.objects.get(mac_address=mac_address)
        client.ip = ip
        client.save()
    except Client.DoesNotExist:
        pass

    return HttpResponse()


@csrf_exempt
@require_POST
def recognition(request: HttpRequest):
    image_data = request.read()
    try:
        results = recognition_face(image_data)

        if results is None:
            raise Exception('Nenhum resultado encontrado.')

        if len(results) != 1:
            raise Exception('Mais de um resultado encontrado.')
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=422)

    try:
        student = Student.objects.get(cpf=results[0][0])
    except Student.DoesNotExist:
        return JsonResponse({'erro': 'Identificador não encontrado no banco de dados.'}, status=422)

    return JsonResponse({
        'name': student.name,
        'enrolment': student.enrolment,
        'class': student.c_lass
    })


@csrf_exempt
@require_POST
def register(request: HttpRequest):
    image_data = request.read()

    if 'x-mac-address' in request.headers:
        mac_address = request.headers['x-mac-address']

        if not utils.is_valid_mac_address(mac_address):
            return HttpResponseForbidden()

    else:
        return HttpResponseForbidden()

    try:
        mac_address = utils.normalize_mac_address(mac_address)
        client = Client.objects.get(mac_address=mac_address)
    except Client.DoesNotExist:
        return JsonResponse({'erro': 'Totem não cadastrado no banco de dados.'}, status=403)

    if client.registering is None or request.content_type is None:
        return HttpResponse()

    try:
        add_face(client.registering, image_data, request.content_type)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=422)

    return HttpResponse()
