
from django.db import models

class Student(models.Model):
    stud_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    room_number = models.IntegerField()

    class Meta:
        ordering = ('stud_id',)
        verbose_name = "Student Data"
        verbose_name_plural = "Student Data"

    def __str__(self):
        return self.first_name + " " + self.last_name

class CoreData(models.Model):
    id = models.AutoField(primary_key=True)
    stud_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    breakfast = models.BooleanField(default=False)
    lunch = models.BooleanField(default=False)
    snack = models.BooleanField(default=False)
    dinner = models.BooleanField(default=False)
    date = models.DateField()

    class Meta:
        ordering = ('id',)
        verbose_name = "Core Data"
        verbose_name_plural = "Core Data"

    def __str__(self):
        return str(self.stud_id.room_number) + "_" + self.stud_id.first_name + "_" + self.stud_id.last_name + "_" + str(self.date)
