from django.http import HttpResponse
from django.template import loader
from .models import Member, Data
import pandas as pd
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from django.http import JsonResponse
from datetime import datetime

def charts(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

def upload_excel(request):
  if request.method == 'POST':
    form = ExcelUploadForm(request.POST, request.FILES)
    if form.is_valid():
      excel_file = request.FILES['excel_file']
      df = pd.read_excel(excel_file, usecols=['SN.', 'Time','Vpv1', 'Vpv2','Ipv1', 'Ipv2', 'Vac1', 'Vac2', 'Vac3', 'Iac1', 'Iac2', 'Iac3', 'Pac', 'E-Total', 'H-Total', 'E-Today', 'Temp'], parse_dates=['Time'])

      # Zmiana nazw kolumn na formę zgodną z modelem Django
      df.columns = ['SN', 'Time','Vpv1', 'Vpv2','Ipv1', 'Ipv2', 'Vac1', 'Vac2', 'Vac3', 'Iac1', 'Iac2', 'Iac3', 'Pac', 'E_Total', 'H_Total', 'E_Today', 'Temp']

      # Dodaj dwie nowe kolumny
      df['date'] = df['Time'].dt.date
      df['time_of_day'] = df['Time'].dt.time

      records = df.to_dict('records')
      Data.objects.bulk_create([Data(**record) for record in records])

      # Usuń wszystkie dane z modelu Data !!!!!!!!!!!!
      #Data.objects.all().delete()
      return redirect('success')  # Przekieruj do strony sukcesu


  else:
    form = ExcelUploadForm()
  return render(request, 'upload_excel.html', {'form': form})



def success(request):
  template = loader.get_template('success.html')
  return HttpResponse(template.render())

def chart_page(request):
  return render(request, 'chart_page.html')


def get_chart_data(request): #udostępnia dane do wykresów
  data = Data.objects.all().order_by('Time')
  #data = Data.objects.all().order_by('Time')[:100] #wyciąga 100 ostatnich rekordów z bazy


  time_labels = [record.Time.strftime('%Y-%m-%d %H:%M:%S') for record in data]
  temperatures = [record.Temp for record in data]
  H_Total = [record.H_Total for record in data]
  E_Total = [record.E_Total for record in data]
  E_Today = [record.E_Today for record in data]

  chart_data = {
    'time_labels': time_labels,
    'temperatures': temperatures,
    'H_Total': H_Total,
    'E_Total': E_Total,
    'E_Today': E_Today,
  }

  return JsonResponse(chart_data)