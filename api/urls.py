
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('student/', views.StudentAPI.as_view()),
    path('data/', views.CoreDataAPI.as_view()),
    path('push/',views.daily_fetch),
]
