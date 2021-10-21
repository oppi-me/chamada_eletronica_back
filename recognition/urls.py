from django.urls import path

from recognition import controllers

urlpatterns = [
    path('adicionar', controllers.add),
    path('reconhecer', controllers.recognition)
]
