
from rest_framework import serializers
from . import models


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = '__all__'

class CoreDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CoreData
        fields = '__all__'


