from django.db import models


class Client(models.Model):
    mac_address = models.CharField(max_length=12, unique=True)
    ip = models.CharField(max_length=15)
    registering = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Student(models.Model):
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    enrolment = models.CharField(max_length=25, unique=True)
    c_lass = models.CharField(max_length=100, null=True, db_column='class')
    shift = models.CharField(max_length=100, null=True)


class Entry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
