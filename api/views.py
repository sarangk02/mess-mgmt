from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from . import models
from .serializer import *

@api_view(['GET'])
def index(request):
    dic = {
        'student/': {
            'GET': {"action":"Get all students"},
            'POST': {"action":'Add new student',"format":"stud_id: int(), first_name: str(50), last_name: str(50), room_number: int()"} ,
            'PATCH': {"action":'Update student with id',"format":"stud_id: int(), first_name: str(50), last_name: str(50), room_number: int()"} ,
            'DELETE': {"action":'Delete student from id',"format":"stud_id: int()"} ,
        },
        'data/': {
            'GET': {"action":"Get all data"},
            'POST': {"action":'Get data between two dates of a student',"format":"stud_id: int(), from: date(), to: date()"} ,
        },
        'push/': {
            'POST': {"action":'Add data for a day',"format":"type: breakfast/lunch/snack/dinner, members: list(int), date: date()"} ,
        },
    }
    return Response({"Available Routes":dic})

class StudentAPI(APIView):
    def get(self, request):
        student_obj = models.Student.objects.all()
        serializer = StudentSerializer(student_obj, many=True)
        return Response({"status:": 200, "payload": serializer.data})

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"status": 403, "message": str(serializer.errors)})
        serializer.save()
        return Response({'message': "Done"})

    def patch(self, request):
        id = request.data['stud_id']
        try:
            student_obj = models.Student.objects.get(stud_id=id)
            serializer = StudentSerializer(student_obj, data=request.data, partial=True)
            if not serializer.is_valid():
                return Response({"status": 403, "message": serializer.errors})
            serializer.save()
            return Response({"status:": 200, "payload": serializer.data, "messae": "your data is saved"})
        except Exception as e:
            return Response({"status": 403, "message": str(e)})

    def delete(self, request):
        id = request.data['stud_id']
        try:
            student_obj = models.Student.objects.get(stud_id=id)
            student_obj.delete()
            return Response({"status:": 200, "message": "your data for id " + str(id) + " is deleted"})
        except Exception as e:
            return Response({"status": 403, "message": str(e)})

class CoreDataAPI(APIView):
    def get(self, request):
        coredata_obj = models.CoreData.objects.all()
        serializer = CoreDataSerializer(coredata_obj, many=True)
        return Response({"status:": 200, "payload": serializer.data})

    def post(self, request):
        data = request.data
        try:
            coredata_obj = models.CoreData.objects.filter(date__range=[data['from'], data['to']], stud_id=data['stud_id'])
            total_breakfast = coredata_obj.filter(breakfast=True).count()
            total_lunch = coredata_obj.filter(lunch=True).count()
            total_snack = coredata_obj.filter(snack=True).count()
            total_dinner = coredata_obj.filter(dinner=True).count()
            serializer = CoreDataSerializer(coredata_obj, many=True)

            payload = {
                "data": serializer.data,
                "count": {
                    "breakfast": total_breakfast,
                    "lunch": total_lunch,
                    "snack": total_snack,
                    "dinner": total_dinner
                }
            }

            return Response({"status:": 200, "payload": payload})
        except Exception as e:
            return Response({"status": 403, "message": str(e)})

@api_view(['POST'])
def daily_fetch(request):
    data = request.data
    if data['type'] == 'breakfast':
        for member_id in data['members']:
            try:
                coredata_obj = models.CoreData(breakfast=True, stud_id_id=member_id, date=data['date'])
                coredata_obj.save()
            except Exception as e:
                return Response({"status": 403, "message": str(e)})
        return Response({"status": 200, "message": "Data saved successfully"})

    elif data['type'] == 'lunch':
        for member_id in data['members']:
            try:
                existing_obj = models.CoreData.objects.filter(stud_id_id=member_id, date=data['date']).exists()
                if existing_obj:
                    existin = models.CoreData.objects.get(stud_id_id=member_id, date=data['date'])
                    existin.lunch = True
                    existin.save()
                else:
                    coredata_obj = models.CoreData(lunch=True, stud_id_id=member_id, date=data['date'])
                    coredata_obj.save()
            except Exception as e:
                return Response({"status": 403, "message": str(e)})
        return Response({"status": 200, "message": "Data saved successfully"})

    elif data['type'] == 'snack':
        for member_id in data['members']:
            try:
                existing_obj = models.CoreData.objects.filter(stud_id_id=member_id, date=data['date']).exists()
                if existing_obj:
                    existin = models.CoreData.objects.get(stud_id_id=member_id, date=data['date'])
                    existin.snack = True
                    existin.save()
                else:
                    coredata_obj = models.CoreData(snack=True, stud_id_id=member_id, date=data['date'])
                    coredata_obj.save()
            except Exception as e:
                return Response({"status": 403, "message": str(e)})
        return Response({"status": 200, "message": "Data saved successfully"})

    elif data['type'] == 'dinner':
        for member_id in data['members']:
            try:
                existing_obj = models.CoreData.objects.filter(stud_id_id=member_id, date=data['date']).exists()
                if existing_obj:
                    existin = models.CoreData.objects.get(stud_id_id=member_id, date=data['date'])
                    existin.dinner = True
                    existin.save()
                else:
                    coredata_obj = models.CoreData(dinner=True, stud_id_id=member_id, date=data['date'])
                    coredata_obj.save()
            except Exception as e:
                return Response({"status": 403, "message": str(e)})
        return Response({"status": 200, "message": "Data saved successfully"})

