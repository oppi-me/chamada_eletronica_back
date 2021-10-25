from django.urls import path

from web import views, controllers

urlpatterns = [
    path('', views.index, name='web/index'),
    path('cadastrar', views.register, name='web/register'),
    path('api/ping', controllers.ping),
    path('api/recognition', controllers.recognition),
    path('api/register', controllers.register)
]
