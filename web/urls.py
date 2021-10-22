from django.urls import path

from web import views

urlpatterns = [
    path('', views.index, name='web/index'),
    path('cadastrar', views.register, name='web/register')
]
