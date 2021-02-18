from django.contrib import admin
from django.urls import path

from . import views
def DesdeApps(self):
    print('desde persona')

urlpatterns = [
    path('persona/', DesdeApps),
    path('api/persona/list', views.UserListApiView.as_view(),),
    path('api/persona/create', views.UserCreateView.as_view(),),
    path('api/persona/detail/<pk>', views.UserDetailView.as_view(),),
    path('api/persona/delete/<pk>', views.UserDeleteView.as_view(),),
    path('api/persona/update/<pk>', views.UserUpdateView.as_view(),),
    path('api/persona/modificar/<pk>', views.UserRetriveUpdateView.as_view(),),
]