from django.shortcuts import render, redirect
from django.contrib.auth import logout as do_logout

def welcome(request):
    return render(request, "users/welcome.html")

def register(request):
    return render(request, "users/register.html")

def login(request):
    return render(request, "users/login.html")

def logout(request):
    # Finalizamos la sesión
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/ggtutbas')

def verificaSession(request):
    return render(request, "ggtutbas/recuperaClave.html")