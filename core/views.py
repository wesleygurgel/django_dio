from django.shortcuts import render, HttpResponse


# Create your views here.

def soma(request, numero_a, numero_b):
    total = numero_a + numero_b
    return HttpResponse('<h1>A soma é {}</h1>'.format(total))
