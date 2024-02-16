from django.shortcuts import render

# Create your views here.


def report(request, *args, **kwargs):
    contexts = {}
    response = render(request, 'report/report.html', contexts)
    return response