from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse
import math

def handler404(request, exception, template_name="404.html"):
    response = render_to_response("core/404.html")
    response.status_code = 404
    return response

def handler500(request, *args, **argv):

    return render(request,'core/500.html')

def flagPais(request):
    """variable para capturar la extension del dominio
        url = request.get_host()
        pais = str(url[-2:])
    """
    ## en desarrollo se coloca la variable enduro

    pais ='cl'

    return (pais)

def obtenerSubdominio(request):
    subdominio = str(request.get_host()).split('.')[0]
    return subdominio

def redondeo(x):
    return int(x + math.copysign(0.5, x))