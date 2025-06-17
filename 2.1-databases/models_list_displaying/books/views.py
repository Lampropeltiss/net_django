from django.shortcuts import render, redirect

from books.models import Book


def index(request):
    return redirect('catalog')


def catalog_view(request):
    template = 'books/catalog.html'
    context = {
        'books': Book.objects.order_by('pub_date'),
        'dates': take_dates(Book.objects.all())
    }
    return render(request, template, context)


def take_dates(books):
    dates = sorted(set(str(book.pub_date) for book in books))
    return dates


def books_view(request, pub_date):
    template = 'books/books_date_list.html'

    previous = Book.objects.order_by('-pub_date').filter(pub_date__lt=pub_date).first()
    next = Book.objects.order_by('pub_date').filter(pub_date__gt=pub_date).first()
    context = {
        'books': Book.objects.filter(pub_date=pub_date),
        'previous': previous,
        'next': next,
    }
    return render(request, template, context)