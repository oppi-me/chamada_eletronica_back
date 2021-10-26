from django.db import models


class ShiftInStudent(models.TextChoices):
    MORNING = 'morning'
    EVENING = 'evening'
    NIGHT = 'night'


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
    shift = models.CharField(max_length=7, choices=ShiftInStudent.choices)

    def get_shift(self) -> ShiftInStudent:
        return ShiftInStudent[self.shift]


class Entry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
