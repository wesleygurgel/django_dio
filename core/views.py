from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento


# Create your views here.

# def index(request):
#     return redirect('/agenda/')


def soma(request, numero_a, numero_b):
    total = numero_a + numero_b
    return HttpResponse('<h1>A soma é {}</h1>'.format(total))


def eventos(request, titulo_evento):
    evento = Evento.objects.get(titulo=titulo_evento)
    print(evento)
    return HttpResponse(
        '<h1>Evento marcado para {} no dia e hórario {}</h1>'.format(evento.usuario, evento.data_evento))


def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.all()
    # Filtro usuario = evento = Evento.objects.filter(usuario=usuario)
    context = {'eventos': evento}
    return render(request, 'agenda.html', context)
