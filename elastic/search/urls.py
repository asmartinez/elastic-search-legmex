from django.urls import path, include
from . import views

urlpatterns = [
    path('search/', views.BuscarDocumento), # URL para busqueda de documento
    path('upload/', views.SubirDocumento), # URL para subir un documento 
    path('document/<int:id>/', views.ModificarDocumento.as_view()),
]
