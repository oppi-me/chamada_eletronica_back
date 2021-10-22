from django.db import models


class Client(models.Model):
    mac_address = models.CharField(max_length=12, unique=True)
    is_registering = models.BooleanField(default=False)
    identifier_record = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        for r in ['.', '-', ':']:
            self.mac_address.replace(r, '')

        super(Client, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                 update_fields=update_fields)


class Student(models.Model):
    name = models.CharField(max_length=255)
    cpf = models.CharField(max_length=11, unique=True)
    matricula = models.CharField(max_length=25, unique=True)
    turma = models.CharField(max_length=100, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        for r in ['.', '-']:
            self.cpf.replace(r, '')

        super(Student, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                  update_fields=update_fields)


class Entry(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
