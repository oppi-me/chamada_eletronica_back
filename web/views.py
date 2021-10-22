from django.contrib import messages
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from recognition.add_face import add_face
from .models import Client, Student
from .utils import is_valid_cpf, is_valid_mac_address


def index(request):
    return render(request, 'web/index.html')


def register(request: HttpRequest):
    if request.method == 'GET':
        return render(request, 'web/register.html')

    if request.method == 'POST':
        cpf = request.POST.get('cpf', default=None)
        mac_address = request.POST.get('mac_address', default=None)

        try:
            client = Client.objects.get(mac_address=mac_address)
            student = Student.objects.get(cpf=cpf)
        except Client.DoesNotExist:
            messages.warning(request, 'Endereço MAC ou aluno não cadastrado.')
            return render(request, 'web/index.html')

        client.is_registering = True
        client.identifier_record = student.cpf
        client.save()

        messages.success(request, 'Modo de cadastro iniciado com sucesso.')

        return render(request, 'web/index.html')

    return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


@csrf_exempt
@require_POST
def add(request: HttpRequest):
    cpf = request.GET.get('cpf', default=None)
    image_data = request.read()

    if cpf is None or not is_valid_cpf(cpf):
        return JsonResponse({'erro': 'CPF inválido'}, status=422)

    try:
        add_face(cpf, image_data, request.content_type)
    except Exception as e:
        return JsonResponse({'erro': str(e)}, status=422)

    return HttpResponse()


@csrf_exempt
@require_POST
def recognition(request: HttpRequest):
    image_data = request.read()
    if 'x-mac-address' in request.headers:
        mac_address = request.headers['x-mac-address']

        if not is_valid_mac_address(mac_address):
            return HttpResponseForbidden()

    else:
        return HttpResponseForbidden()

    # try:
    #     add_face(cpf, image_data, request.content_type)
    # except Exception as e:
    #     return JsonResponse({'erro': str(e)}, status=422)

    return HttpResponse()
