from django.shortcuts import render, redirect

from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    sort_by = request.GET.get('sort', 'name')
    phones = Phone.objects.all()
    sorted_phones = sort_phones(phones, sort_by)

    template = 'catalog.html'
    context = {
        'phones': sorted_phones
    }
    return render(request, template, context)


def sort_phones(phones, sort_by):
    if sort_by == 'min_price':
        sorted_phones = phones.order_by('price')
    elif sort_by == 'max_price':
        sorted_phones = phones.order_by('price').reverse()
    else:
        sorted_phones = phones.order_by('name')
    return sorted_phones


def show_product(request, slug):
    template = 'product.html'
    context = {
        'phone': Phone.objects.get(slug=slug)
    }
    return render(request, template, context)
