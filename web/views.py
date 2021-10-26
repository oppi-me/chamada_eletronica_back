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
        mac_address = request.POST.get('mac_address', default='')

        cpf = utils.sanitize(cpf)

        try:
            client = Client.objects.get(mac_address=mac_address)
            student = Student.objects.get(cpf=cpf)
        except (Client.DoesNotExist, Student.DoesNotExist):
            messages.warning(request, 'Aluno ou endereço MAC não cadastrado.')
            return redirect('web/index')

        if client.registering:
            client.registering = None
            client.save()

            messages.success(request, 'Modo de captura encerrado.')
            return redirect('web/index')

        client.registering = student.cpf
        client.save()

        messages.success(request, 'Modo de captura iniciado.')
        return redirect('web/index')

    return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def register(request: HttpRequest):
    if request.method == 'GET':
        return redirect('web/index')

    if request.method == 'POST':
        name = request.POST.get('name', default='')
        cpf = request.POST.get('cpf', default='')
        enrolment = request.POST.get('enrolment', default='')
        c_lass = request.POST.get('class', default='')
        shift = request.POST.get('shift', default='')

        if not (name and cpf and enrolment and c_lass and shift):
            messages.warning(request, 'Não deixe campos vazios.')
            return redirect('web/index')

        if not utils.is_valid_cpf(cpf):
            messages.warning(request, 'CPF inválido.')
            return redirect('web/index')

        try:
            Student.objects.create(
                name=name,
                cpf=utils.sanitize(cpf),
                enrolment=enrolment,
                c_lass=c_lass,
                shift=shift
            )
        except IntegrityError:
            messages.warning(request, 'Não foi possível cadastrar o aluno.')
            return redirect('web/index')

        messages.success(request, 'Aluno cadastrado com sucesso.')
        return redirect('web/index')

    return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
