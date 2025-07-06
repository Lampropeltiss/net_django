from django.shortcuts import render

from articles.models import Article


def articles_list(request):
    template = 'articles/news.html'
    ordering = '-published_at'
    articles = Article.objects.all()
    context = {
        'object_list': articles.order_by(ordering)
    }
    return render(request, template, context)
