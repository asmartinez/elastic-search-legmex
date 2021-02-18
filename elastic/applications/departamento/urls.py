from django.contrib import admin
from django.urls import path

def DesdeApps(self):
    print('desde departamento')

urlpatterns = [
    path('departamento/', DesdeApps),
]