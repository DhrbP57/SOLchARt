from django.urls import path
from . import views

urlpatterns = [
    path('charts/', views.charts, name='charts'),
    path('success/', views.success, name='success'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('', views.index, name='index'),
]