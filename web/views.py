from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpRequest, HttpResponseNotAllowed
from django.shortcuts import render, redirect

from . import utils
from .models import Client, Student


def index(request):
    clients = Client.objects.all()
    students = Student.objects.all()

    students_total = len(students)

    return render(
        request,
        'web/index.html', {
            'clients': clients,
            'students_total': students_total
        }
    )


def capture(request: HttpRequest):
    if request.method == 'GET':
        return redirect('web/index')

    if request.method == 'POST':
        cpf = request.POST.get('cpf', default='')
        mac_address = request.POST.get('mac_address', default=None)
        stop = request.POST.get('stop', default=False)

        if stop:
            client = Client.objects.get(mac_address=mac_address)
            client.registering = None
            client.save()
            messages.success(request, 'Modo captura encerrado com sucesso.')
            return redirect('web/index')

        cpf = utils.sanitize(cpf)
        mac_address = utils.normalize_mac_address(mac_address)

        try:
            client = Client.objects.get(mac_address=mac_address)
            student = Student.objects.get(cpf=cpf)
        except (Client.DoesNotExist, Student.DoesNotExist):
            messages.warning(request, 'Endereço MAC ou aluno não cadastrado.')
            return redirect('web/index')

        client.is_registering = True
        client.registering = student.cpf
        client.save()

        messages.success(request, 'Modo de captura iniciado com sucesso.')

        return redirect('web/index')

    return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def register(request: HttpRequest):
    if request.method == 'GET':
        return redirect('web/index')

    if request.method == 'POST':
        name = request.POST.get('name', default=None)
        cpf = request.POST.get('cpf', default=None)
        enrolment = request.POST.get('enrolment', default=None)
        c_lass = request.POST.get('class', default=None)
        shift = request.POST.get('shift', default=None)

        if name is None or \
                cpf is None or \
                enrolment is None or \
                c_lass is None or \
                shift is None:
            messages.warning(request, 'Não deixe campos vazios.')
            return redirect('web/index')

        if not utils.is_valid_cpf(cpf):
            messages.warning(request, 'CPF inválido.')
            return redirect('web/index')

        cpf = utils.sanitize(cpf)

        try:
            Student.objects.create(name=name, cpf=cpf, enrolment=enrolment, c_lass=c_lass, shift=shift)
        except IntegrityError:
            messages.warning(request, 'Não foi possível cadastrar o aluno.')
            return redirect('web/index')

        messages.success(request, 'Aluno cadastrado com sucesso.')

        return redirect('web/index')

    return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
