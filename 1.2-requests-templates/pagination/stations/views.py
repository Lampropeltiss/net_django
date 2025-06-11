from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse

DATA = 'data-398-2018-08-30.csv'


def index(request):
    return redirect(reverse('bus_stations'))


def bus_stations(request):
    page_number = int(request.GET.get('page', 1))
    paginator = Paginator(read_csv(DATA), 10)
    page = paginator.get_page(page_number)

    context = {
        'bus_stations': page,
        'page': page,
    }
    return render(request, 'stations/index.html', context)


def read_csv(file):
    import csv
    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = [r for r in reader]
        return rows
