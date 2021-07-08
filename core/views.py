from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponse, redirect
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http.response import Http404, JsonResponse
from datetime import datetime, timedelta


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


@login_required(login_url='/login/')
def lista_eventos(request):
    usuario = request.user
    # evento = Evento.objects.all()
    data_atual = datetime.now() - timedelta(hours=1)
    print(data_atual)

    eventos_futuros = Evento.objects.filter(usuario=usuario, data_evento__gt=data_atual)
    eventos_atrasados = Evento.objects.filter(usuario=usuario, data_evento__lt=data_atual)

    context = {'eventos_futuros': eventos_futuros,
               'evento_atrasados': eventos_atrasados}
    return render(request, 'agenda.html', context)


def login_user(request):
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, 'Usuario ou senha inválido!')

    return redirect('/')


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        local = request.POST.get('local')
        descricao = request.POST.get('descricao')
        id_evento = request.POST.get('id_evento')
        usuario = request.user

        if id_evento:
            event = Evento.objects.get(id=id_evento)
            if event.usuario == usuario:
                event.titulo = titulo
                event.descricao = descricao
                evento.data_evento = data_evento
                event.local = local
                event.save()

        else:
            Evento.objects.create(titulo=titulo, data_evento=data_evento, descricao=descricao, local=local,
                                  usuario=usuario)

    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    user = request.user
    try:
        event = Evento.objects.get(id=id_evento)
    except Exception:
        raise Http404()

    if user == event.usuario:
        event.delete()
    else:
        raise Http404()

    return redirect('/')


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)


@login_required(login_url='/login/')
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)

    event = Evento.objects.filter(usuario=usuario).values('id', 'titulo')

    context = {'eventos': evento}
    return JsonResponse(list(event), safe=False)

