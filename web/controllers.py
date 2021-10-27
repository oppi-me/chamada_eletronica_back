from datetime import datetime, timedelta

from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from recognition.add_face import add_face
from recognition.recognition_face import recognition_face
from . import utils
from .models import Client, Student, Entry, Config


@csrf_exempt
@require_POST
def ping(request: HttpRequest):
    ip = utils.get_ip(request)
    mac_address = utils.get_mac_address(request)

    if not utils.is_valid_mac_address(mac_address):
        return HttpResponseBadRequest()

    client = Client.objects.get_or_create(mac_address=mac_address)[0]


    client.ip = ip
    client.save()

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
        'shift': student.shift.name
    })


@csrf_exempt
@require_POST
def register(request: HttpRequest):
    image_data = request.read()
    mac_address = utils.get_mac_address(request)

    try:
        client = Client.objects.get(mac_address=mac_address)
        student = client.student

        if not student or request.content_type is None:
            return HttpResponse()

        add_face(student.cpf, image_data, request.content_type)
        student.photos += 1
        student.save()

    except Client.DoesNotExist:
        return JsonResponse({'erro': 'Totem não encontrado no banco de dados.'}, status=403)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=422)

    return HttpResponse()


@csrf_exempt
def __make_entry(client, student):
    current_time = datetime.now()

    entry = Entry.objects.filter(created_at__day=current_time.day, student=student)

    if len(entry) > 0:
        return

    entry_tolerance = int(Config.objects.get(key='entry_tolerance').value)
    shift_open = datetime.combine(current_time.date(), student.shift.open) + timedelta(minutes=entry_tolerance)

    if current_time > shift_open:
        raise Exception('Entrada negada.')
    else:
        Entry.objects.create(student=student, client=client)
