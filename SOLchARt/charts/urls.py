from django.urls import path
from . import views


urlpatterns = [
    path('charts/', views.charts, name='charts'),
    path('chart_page/', views.chart_page, name='chart_page'),
    path('get_chart_data/', views.get_chart_data, name='get_chart_data'),
    path('success/', views.success, name='success'),
    path('upload_excel/', views.upload_excel, name='upload_excel'),
    path('', views.index, name='index'),
]