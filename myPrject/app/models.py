from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Korisnik(AbstractUser):
    ROLES = (('prof', 'profesor'), ('stu', 'student'), ('admin', 'admin'))
    STATUS = (('none', 'None'), ('izv', 'izvanredni student'),
              ('red', 'redovni student'))
    role = models.CharField(max_length=50, choices=ROLES, default='stu')
    status = models.CharField(max_length=50, choices=STATUS, default='none')

    def readable_status(self):
        return dict(self.STATUS)[self.status]

    def readable_role(self):
        return dict(self.ROLES)[self.role]

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


class Predmeti(models.Model):
    IZBORNI = (('da', 'da'), ('ne', 'ne'))
    name = models.CharField(max_length=50)
    kod = models.CharField(max_length=50)
    program = models.CharField(max_length=50)
    ects = models.IntegerField()
    sem_red = models.IntegerField()
    sem_izv = models.IntegerField()
    izborni = models.CharField(max_length=50, choices=IZBORNI)


class UpisniList(models.Model):
    STATUS = (('up', 'upisan'), ('po', 'polozen'), ('ip', 'izgubio potpis'))
    student = models.ForeignKey(
        Korisnik, on_delete=models.CASCADE, limit_choices_to={'role': 'stu'})
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, choices=STATUS)

    class Meta:
        unique_together = ('student', 'predmet')

    def readable_status(self):
        return dict(self.STATUS)[self.status]


class AssignedCourse(models.Model):
    profesor = models.ForeignKey(Korisnik, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('profesor', 'predmet')
