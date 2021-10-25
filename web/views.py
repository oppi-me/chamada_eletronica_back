from django.contrib import messages
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render

from .models import Client, Student


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
        client.registering = student.cpf
        client.save()

        messages.success(request, 'Modo de cadastro iniciado com sucesso.')

        return render(request, 'web/index.html')

    return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
