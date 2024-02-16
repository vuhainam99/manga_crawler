from django.shortcuts import render

# Create your views here.


def crawl(request, *args, **kwargs):
    contexts = {}
    response = render(request, 'crawl/crawl.html', contexts)
    return response