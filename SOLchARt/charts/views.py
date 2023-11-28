from django.http import HttpResponse
from django.template import loader
from .models import Member, Data
import pandas as pd
from django.shortcuts import render, redirect
from .forms import ExcelUploadForm
from django.http import JsonResponse
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.db.models import Max, Min, Avg


@login_required
def charts(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

@login_required
def index(request):
  template = loader.get_template('index.html')
  return HttpResponse(template.render())

@login_required
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

      # Pobierz aktualnie zalogowanego użytkownika
      current_user = request.user

      # Dodaj dwie nowe kolumny związane z użytkownikiem
      df['user_id'] = current_user.id

      records = df.to_dict('records')
      Data.objects.bulk_create([Data(**record) for record in records])

      # Usuń wszystkie dane z modelu Data !!!!!!!!!!!!
      #Data.objects.all().delete()
      return redirect('success')  # Przekieruj do strony sukcesu


  else:
    form = ExcelUploadForm()
  return render(request, 'upload_excel.html', {'form': form})



@login_required
def success(request):
  template = loader.get_template('success.html')
  return HttpResponse(template.render())

@login_required
def chart_page(request):
  return render(request, 'chart_page.html')



@login_required
def get_chart_data(request): #udostępnia dane do wykresów
  current_user = request.user

  # Ogranicz zapytanie do bazy danych do rekordów zalogowanego użytkownika i tych, które zostały udostępnione przez niego
  data = Data.objects.filter(user=current_user).order_by('Time')
  #data = Data.objects.all().order_by('Time')
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

@login_required
def extremum_values(request):
    # Znajdź największe i najmniejsze wartości dla poszczególnych pól tylko dla zalogowanego użytkownika
    extremum_data = Data.objects.filter(user=request.user).aggregate(
        max_temp=Max('Temp'),
        min_temp=Min('Temp'),
        avg_temp=Avg('Temp'),
        max_date=Max('date'),
        min_date=Min('date'),
        max_time_of_day=Max('time_of_day'),
        min_time_of_day=Min('time_of_day'),
        max_e_today=Max('E_Today'),
        min_e_today=Min('E_Today'),
        max_e_total=Max('E_Total'),
        min_e_total=Min('E_Total'),
        max_h_total=Max('H_Total'),
        min_h_total=Min('H_Total'),
    )

    # Oblicz średnią temperaturę dla każdego dnia
    avg_temp_per_day = Data.objects.filter(user=request.user).values('date').annotate(avg_temp=Avg('Temp'))

    # Znajdź datę, kiedy wystąpiła najwyższa temperatura
    time_of_max_temp_data = Data.objects.filter(user=request.user, Temp=extremum_data['max_temp']).values('Time').first()
    time_of_min_temp_data = Data.objects.filter(user=request.user, Temp=extremum_data['min_temp']).values('Time').first()

    # Przygotuj dane do przekazania do szablonu
    context = {
        'max_temp': extremum_data['max_temp'],
        'min_temp': extremum_data['min_temp'],
        'avg_temp': extremum_data['avg_temp'],
        'max_date': extremum_data['max_date'],
        'min_date': extremum_data['min_date'],
        'max_time_of_day': extremum_data['max_time_of_day'],
        'min_time_of_day': extremum_data['min_time_of_day'],
        'max_e_today': extremum_data['max_e_today'],
        'min_e_today': extremum_data['min_e_today'],
        'max_e_total': extremum_data['max_e_total'],
        'min_e_total': extremum_data['min_e_total'],
        'max_h_total': extremum_data['max_h_total'],
        'min_h_total': extremum_data['min_h_total'],
        'time_of_max_temp': time_of_max_temp_data['Time'] if time_of_max_temp_data else None,
        'time_of_min_temp': time_of_min_temp_data['Time'] if time_of_min_temp_data else None,
        'avg_temp_per_day': avg_temp_per_day,
    }

    # Renderuj szablon z danymi
    return render(request, 'extremum_values.html', context)