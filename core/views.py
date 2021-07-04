from django.shortcuts import render, HttpResponse
from core.models import Evento

# Create your views here.

def soma(request, numero_a, numero_b):
    total = numero_a + numero_b
    return HttpResponse('<h1>A soma é {}</h1>'.format(total))


def eventos(request, titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    print(evento)
    return HttpResponse('<h1>Evento marcado para {} no dia e hórario {}</h1>'.format(evento.usuario, evento.data_evento))
