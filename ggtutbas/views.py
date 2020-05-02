import json
import string
import random
import datetime
import urllib.parse
import urllib.request
import socket
from django.shortcuts import render, redirect
from django.views.generic import View
from .render import Render
from django.http import HttpResponse
from ggalbas.models import TblListas, TblTutores, TblPreguntausuarios, TblInstituciones, TblAlumnos, TblSubproducto, TblContenidoUnidad, TblContenidos, TblUnidades, TblPlan, TblContenidosObjetivos, TblTutorInstitucion, TblPlanAutonomo, TblTarjetas
from core.views import flagPais, obtenerSubdominio

def variablesPais(request):
    pais=flagPais(request)
    #declaracion de variables de acuerdo a pais, por defecto se setea CL
    if str(pais)=='pe':
        rut= 'Id usuario'
        curso='Sección'
        textoInicio='Bienvenidos(as) al programa EMAT. Desde este libro podrás observar en «Resumen Colegio», los resultados generales de todas las secciones que trabajan en EMAT Guiado. Para conocer los resultados específicos de las secciones asignadas, debes seleccionar la sección para habilitar el menú.'
        cursoPdf='Primaria'
        menuResultadosCurso='Resultados sección'
        menuPlanificacion='Competencia / Desempeño'
        textoAlumnoDiferenciado='Esta sección cuenta con el complemento de EMAT Diferenciado. En la edición de datos puedes cambiar el plan de trabajo de un estudiante de regular a diferenciado y viceversa.'
        textoAlumnoAutonomo= 'Al elegir la opción de activar unidades en el plan de trabajo de la sección, puedes otorgarle a los estudiantes aventajados, la modalidad de alumnos autónomos.'
        promedioAutonomo='18'
        popAutonomo='Una vez otorgada esta modalidad de trabajo a un estudiante, se le activarán todas las unidades, mientras que el resto de la sección avanzara de acuerdo a las unidades activadas por el profesor.'
        oa1='Competencia / Desempeño'
        oa2=''
        activarAlert='Si quieres modificar el plan de trabajo de la sección, puedes hacerlo en Ítem “orden contenidos”. Te recomendamos hacerlo antes del inicio de actividades con los alumnos ya que si  un alumno inicia una actividad dentro de un contenido, este no podrá ser modificado.'
    elif str(pais)=='cl':
        rut= 'Rut'
        curso='Curso'
        textoInicio='Bienvenidos(as) al programa EMAT. Desde este libro podrás observar en «Resumen Colegio», los resultados generales de todos los cursos que trabajan en EMAT Guiado. Para conocer los resultados específicos de los cursos asignados, debes seleccionar el curso para habilitar el menú.'
        cursoPdf = 'Basica'
        menuResultadosCurso='Resultados curso'
        menuPlanificacion='Objetivos de aprendizaje'
        textoAlumnoDiferenciado = 'Este curso cuenta con el complemento de EMAT Diferenciado. En la edición de datos puedes cambiar el plan de trabajo de un estudiante de regular a diferenciado y viceversa.'
        textoAlumnoAutonomo = 'Al elegir la opción de activar unidades en el plan de trabajo del curso, puedes otorgarle a los estudiantes aventajados, la modalidad de alumnos autónomos.'
        promedioAutonomo = '6,5'
        popAutonomo='Una vez otorgada esta modalidad de trabajo a un estudiante, se le activarán todas las unidades, mientras que el resto del curso avanzara de acuerdo a las unidades activadas por el profesor.'
        oa1='Obj.'
        oa2='Aprendizaje'
        activarAlert = 'Si quieres modificar el plan de trabajo del curso, puedes hacerlo en Ítem “orden contenidos”. Te recomendamos hacerlo antes del inicio de actividades con los alumnos ya que si  un alumno inicia una actividad dentro de un contenido, este no podrá ser modificado.'
    else:
        rut= 'Rut'
        curso='Curso'
        textoInicio = 'Bienvenidos(as) al programa EMAT. Desde este libro podrás observar en «Resumen Colegio», los resultados generales de todos los cursos que trabajan en EMAT Guiado. Para conocer los resultados específicos de los cursos asignados, debes seleccionar el curso para habilitar el menú.'
        cursoPdf = 'Basica'
        menuResultadosCurso='Resultados curso'
        menuPlanificacion = 'Objetivos de aprendizaje'
        textoAlumnoDiferenciado = 'Este curso cuenta con el complemento de EMAT Diferenciado. En la edición de datos puedes cambiar el plan de trabajo de un estudiante de regular a diferenciado y viceversa.'
        textoAlumnoAutonomo = 'Al elegir la opción de activar unidades en el plan de trabajo del curso, puedes otorgarle a los estudiantes aventajados, la modalidad de alumnos autónomos.'
        promedioAutonomo = '6,5'
        popAutonomo = 'Una vez otorgada esta modalidad de trabajo a un estudiante, se le activarán todas las unidades, mientras que el resto del curso avanzara de acuerdo a las unidades activadas por el profesor.'
        oa1='Obj.'
        oa2='Aprendizaje'
        activarAlert = 'Si quieres modificar el plan de trabajo del curso, puedes hacerlo en Ítem “orden contenidos”. Te recomendamos hacerlo antes del inicio de actividades con los alumnos ya que si  un alumno inicia una actividad dentro de un contenido, este no podrá ser modificado.'

    data={
        'rut':rut,
        'curso':curso,
        'textoInicio':textoInicio,
        'cursoPdf': cursoPdf,
        'menuResultadosCurso': menuResultadosCurso,
        'menuPlanificacion': menuPlanificacion,
        'textoAlumnoDiferenciado': textoAlumnoDiferenciado,
        'textoAlumnoAutonomo': textoAlumnoAutonomo,
        'promedio': promedioAutonomo,
        'popAutonomo': popAutonomo,
        'oa1': oa1,
        'oa2': oa2,
        'activarAlert': activarAlert,
        'pais': pais,
    }

    return (data)

def index(request):
    variables=variablesPais(request)
    data={
        'variables':variables,
    }
    return render(request, 'ggtutbas/login.html', data)

def validaIngreso(request):
    rut = request.POST['rut']
    codColegio = request.POST['codColegio']
    password = request.POST['password']
    consultaRbd = TblInstituciones.objects.filter(rbd=codColegio)
    pais = flagPais(request)
    respuesta = {}

    if consultaRbd:
        respuesta['rbd'] = True
        consultaListaTutor= TblListas.objects.filter(rbd=codColegio, rut_tutor=rut)
        if consultaListaTutor:
            respuesta['listaTutor']= True
            consultaRut = TblTutores.objects.filter(rut_tutor=rut, clave__regex=password)
            if consultaRut:
                respuesta['user'] = True
                request.session['rut'] = consultaRut[0].rut_tutor
                request.session['fullName'] = consultaRut[0].nombres + ' ' + consultaRut[0].apellidos
                request.session['rbd'] = consultaRbd[0].rbd
                request.session['nombreColegio'] = consultaRbd[0].nombre_institucion
                request.session['rbd'] = consultaRbd[0].rbd
                request.session['pais'] =str(pais)
            else:
                respuesta['user'] = False
        else:
            respuesta['listaTutor'] = False
    else:
        respuesta['rbd'] = False

    responde = json.dumps(respuesta)

    return HttpResponse(responde)

def registroTutor(request):
    variables=variablesPais(request)
    preguntas = TblPreguntausuarios.objects.all()
    data={
        'variables':variables,
        'preguntas': preguntas,
    }


    return render(request, 'ggtutbas/nuevoTutor.html', data)

def agregarTutor(request):
    rut = request.POST['rut']
    codColegio = request.POST['codColegio']
    codUsuario = request.POST['codUsuario']
    email = request.POST['email']
    nombres = request.POST['nombres']
    apellidos = request.POST['apellidos']
    password = request.POST['password']
    pregunta = TblPreguntausuarios.objects.get(id_pregunta=int(request.POST['pregunta']))
    respuestaSecuridad = request.POST['respuesta'].upper()
    respuesta = {}
    if (request.POST['telefono'] == ''):
        telefono = 0
    else:
        telefono = request.POST['telefono']

    ##se consulta si el rut ingresado pertenece a algun tutor inscrito
    consulta = TblTutores.objects.filter(rut_tutor=rut)

    if consulta:
        respuesta['rut'] = 'existe'
    else:
        consultaRbd = TblInstituciones.objects.filter(rbd=codColegio)
        if consultaRbd:
            respuesta['rbd'] = True
            ##se consulta si el codigo usuario pertenece a algun tutor inscrito
            consultaTarjeta = TblTarjetas.objects.filter(codigo_usuario=codUsuario, rbd=codColegio, estado_tarjeta=1, tipo_tarjeta=1)

            if consultaTarjeta:
                respuesta['codUser'] = 'no'
                guardaTutor = TblTutores(rut_tutor=rut, nombres=nombres, apellidos=apellidos, correo=email,
                                         telefono=telefono, clave=password, codigo_usuario=codUsuario,
                                         id_pregunta=pregunta, respuesta=respuestaSecuridad)

                try:
                    guardaTutor.save()
                    respuesta['tutor'] = 'ok'
                except:
                    respuesta['status'] = 'error1'

                tutorRegistrado = TblTutores.objects.filter(rut_tutor=rut)
                if tutorRegistrado:
                    respuesta['password'] = tutorRegistrado[0].clave
                    try:
                        consultaTarjeta.update(estado_tarjeta=0)
                    except:
                        respuesta['status'] = 'error2'
                    tutorInstitucion = TblTutorInstitucion(rut_tutor=TblTutores.objects.get(rut_tutor=tutorRegistrado[0].rut_tutor),rbd=TblInstituciones.objects.get(rbd=codColegio))
                    try:
                        tutorInstitucion.save()
                        respuesta['tutorInstituto'] = True
                    except:
                        respuesta['tutorInstituto'] = False
                else:
                    respuesta['status'] = 'error1'
            else:
                respuesta['codUser'] = 'existe'

        else:
            respuesta['rbd'] = False

    responde = json.dumps(respuesta)

    return HttpResponse(responde)


def recuperaClave(request):
    variables=variablesPais(request)
    data={
        'variables':variables,
    }
    return render(request, 'ggtutbas/recuperaClave.html', data)


def verificaRut(request):
    rut = request.POST['rut']
    consulta = TblTutores.objects.filter(rut_tutor=rut)
    respuesta = {}
    if consulta:
        preguntaUser = TblPreguntausuarios.objects.filter(id_pregunta=int(str(consulta[0].id_pregunta)))
        if preguntaUser:
            respuesta['pregunta'] = preguntaUser[0].pregunta
            respuesta['status'] = 'consulta ok'
    else:
        respuesta['status'] = 'error'
    responde = json.dumps(respuesta)
    return HttpResponse(responde)


def verificaRespuesta(request):
    rut = request.POST['rut']
    answer = request.POST['answer']
    consulta = TblTutores.objects.filter(rut_tutor=rut, respuesta=answer.upper())
    respuesta = {}
    if consulta:
        respuesta['status'] = 'respuesta ok'
        respuesta['password'] = consulta[0].clave
    else:
        respuesta['status'] = 'error'
    responde = json.dumps(respuesta)
    return HttpResponse(responde)


def menuPrincipal(request):
    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        del request.session["curso"]

    fullName = request.session['fullName']
    listas = TblListas.objects.filter(rut_tutor=rut)
    variables=variablesPais(request)
    data = {
        'rut': rut,
        'fullName': fullName,
        'listas': listas,
        'nombreColegio': colegio,
        'variables': variables,

    }

    return render(request, 'ggtutbas/menuPrincipal.html', data)

def resumenColegio(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'


    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, hoja= 're')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)

def detalleAlumno(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista= request.GET['codLista']

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'



    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, codLista=codLista, hoja= 'da')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)

def notaMensual(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista= request.GET['codLista']

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, codLista=codLista, hoja= 'no')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)

def distribucionResultado(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista= request.GET['codLista']

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, codLista=codLista, hoja= 'dr')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)

def descripcionEvaluacionesAnuales(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista= request.GET['codLista']

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'


    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, codLista=codLista, hoja= 'de')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)

def diagnosticoEvaluacionesAnuales(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista= request.GET['codLista']

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, codLista=codLista, hoja= 'di')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)


def pruebaIntEvaluacionesAnuales(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista= request.GET['codLista']

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, codLista=codLista, hoja= 'pi')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)

def contenidoEvaluacionesParciales(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista= request.GET['codLista']

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, codLista=codLista, hoja= 'pc')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)

def avanceResultadosCurso(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    if request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista= request.GET['codLista']

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'http://reportes2.e-mat.cl/guireportes/index/'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'http://reportes.e-mat.pe/guireportes/index/'

    else:
        var_server_destino = 'http://reportesdes.e-mat.cl/guireportes/index/'

    url = var_server_destino
    d=dict(rut=rut, rbd=rbd, codLista=codLista, hoja= 'ar')
    f= urllib.parse.urlencode(d)
    f=f.encode('utf-8')
    req = urllib.request.Request(url, f)
    response = urllib.request.urlopen(req)
    the_page = response.read()

    return HttpResponse(the_page)


def consultaListas(request):
    if request.session.get("rut", False):
        rut = request.session['rut']
    else:
        return redirect('/ggtutbas')
    listas = TblListas.objects.filter(rut_tutor=rut).order_by('id_nivel', 'letra')
    pais=request.session['pais']
    respuesta={}
    data = dict()
    respuesta['pais']=pais
    for lista in listas:
        data[lista.codigo_lista] = str(lista.id_nivel.nivel) + '-' + str(lista.letra)
    respuesta['codigoLista']=data

    responde = json.dumps(respuesta)

    return HttpResponse(responde)

def sessionCurso(request):
    request.session['curso'] = request.POST['idLista']
    respuesta = {'status': 'ok'}
    responde = json.dumps(respuesta)

    return HttpResponse(responde)


def descripcionAnual(request):
    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
    elif 'rut' in request.GET:
        rut = request.GET['rut']
        colegio = 'nombre del colegio'
    else:
        return redirect('/ggtutbas')

    if request.session.get("fullName", False):
        fullName = request.session['fullName']
    else:
        fullName = request.GET['fullName']

    if 'codLista' in request.GET:
        codLista = request.GET['codLista']
        request.session['curso'] = codLista
    else:
        codLista = request.session['curso']


    nivel = TblListas.objects.get(codigo_lista=codLista)
    variables = variablesPais(request)


    data = {
        'rut': rut,
        'fullName': fullName,
        'codLista': codLista,
        'nivel': nivel.id_nivel.numero_nivel,
        'nombreColegio': colegio,
        'variables':variables,

    }
    return render(request, 'ggtutbas/plan_descrip_anual.html', data)

def descripcionContenidos(request):
    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
    else:
        return redirect('/ggtutbas')

    fullName = request.session['fullName']

    if 'codLista' in request.GET:
        codLista = request.GET['codLista']
        request.session['curso'] = codLista
    else:
        codLista = request.session['curso']

    nivel = TblListas.objects.get(codigo_lista=codLista)
    variables= variablesPais(request)

    data = {
        'rut': rut,
        'fullName': fullName,
        'codLista': codLista,
        'nivel': nivel.id_nivel.numero_nivel,
        'nombreColegio': colegio,
        'variables': variables,

    }
    return render(request, 'ggtutbas/plan_descrip_contenidos.html', data)

def datosAlumno(request):
    if request.session.get("rut", False):
        rut = request.session['rut']
        colegio = request.session['nombreColegio']
    else:
        return redirect('/ggtutbas')

    fullName = request.session['fullName']

    if 'codLista' in request.GET:
        codLista = request.GET['codLista']
        request.session['curso'] = codLista
    else:
        codLista = request.session['curso']


    listaActual = TblListas.objects.filter(codigo_lista=codLista)

    ## Se verifica si la lista tiene asociado emat diferenciado
    if listaActual[0].id_producto.id_producto == 3:
        displayDiferenciado = 'flex;'
        columnaDiferenciada = 1

        cantAlumnos = len(TblAlumnos.objects.filter(codigo_lista=listaActual[0].codigo_lista,
                                                    id_producto=listaActual[0].id_producto.id_producto))
        listaDiferencia = True

    else:
        displayDiferenciado = 'none;'
        listaDiferencia = False
        columnaDiferenciada = 0
    # Se verifica si la la activacion esta de 1-1 o todas activas
    if listaActual[0].activar_unidades == 1:
        displayAutonomo='flex'
        columnaAutonomo = 1
    else:
        displayAutonomo = 'none'
        columnaAutonomo= 0

    ##return HttpResponse(displayAutonomo)
    variables = variablesPais(request)



    data = {
        'rut': rut,
        'fullName': fullName,
        'nombreColegio': colegio,
        'listaDiferencia': listaDiferencia,
        'nivel': listaActual[0].id_nivel.numero_nivel,
        'codLista': codLista,
        'displayDiferenciado':displayDiferenciado,
        'columnaDiferenciada': columnaDiferenciada,
        'displayAutonomo': displayAutonomo,
        'columnaAutonomo': columnaAutonomo,
        'letra': listaActual[0].letra,
        'variables': variables,
    }
    return render(request, 'ggtutbas/plan_datos_alumno.html', data)

def listarPreguntaUsuarios(request):
    objPreguntas = TblPreguntausuarios.objects.all().order_by('pregunta')
    listaPreguntas = '<option value="">Seleccione pregunta</option>'
    for result in objPreguntas:
        listaPreguntas += '<option value="'+str(result.id_pregunta)+'">'+str(result.pregunta)+'</option>'
    return HttpResponse(listaPreguntas)

def guardarAlumno(request):
    codigo_lista = request.session['curso']
    rut = request.POST['rut']+'-'+request.POST['validador']
    nombre = request.POST['nombre'].upper()
    apellido = request.POST['apellido'].upper()
    respuesta = request.POST['respuesta'].upper()
    ##caracteres = string.ascii_letters + string.digits
    ##clave = ''.join(random.choice(caracteres) for _ in range(6))
    clave=random.randrange(1000, 9999)
    now = datetime.datetime.now()
    fecha_registro = now.strftime("%Y-%m-%d %H:%M:%S")
    responde = {'estatus': 1, 'mensaje': '', 'clave': ''}
    objLista = TblListas.objects.get(codigo_lista=str(codigo_lista))

    # validar que el rut no se encuentre registrado en DB.
    cantidadAlumno = len(TblAlumnos.objects.filter(rut_alumno=rut))

    if cantidadAlumno == 0:
        # verifica que hay cupo disponible.
        if int(objLista.alumnos_registrados) < int(objLista.total_alumnos):

            registroAlumno = TblAlumnos(rut_alumno=rut,
                                        nombre=nombre,
                                        apellido=apellido,
                                        clave=clave,
                                        id_pregunta=TblPreguntausuarios.objects.get(id_pregunta=int(request.POST['id_pregunta'])),
                                        respuesta=respuesta,
                                        id_producto=TblSubproducto.objects.get(id_producto=2),
                                        activo=1,
                                        nuevo=1,
                                        autonomo=0,
                                        fecha_registro=fecha_registro,
                                        codigo_lista=TblListas.objects.get(codigo_lista=str(codigo_lista)), libre=0)

            # actualiza alumnos inscritos.
            objLista.alumnos_registrados = int(objLista.alumnos_registrados) + 1

            try:
                registroAlumno.save()
                objLista.save()
                responde['clave'] = clave
            except:
                responde['estatus'] = 0
                responde['mensaje'] = 'Ocurrio un error, intente nuevamente.'
        else:
            responde['estatus'] = 0
            responde['mensaje'] = 'no hay cupo.'
    else:
        responde['estatus'] = 0
        responde['mensaje'] = 'El rut ingresado ya se encuentra registrado.'

    return HttpResponse(json.dumps(responde))

def editarAlumno(request):
    rut = request.POST['rutAlumno']
    nombre = request.POST['nombreAlumno'].upper()
    apellido = request.POST['apellidoAlumno'].upper()
    id_producto_diferenciado = 3
    id_producto_regular = 2
    responde = {'estatus': 1, 'mensaje': ''}
    now = datetime.datetime.now()
    fecha_registro = now.strftime("%Y-%m-%d %H:%M:%S")

    if 'id_producto' in request.POST:
        id_producto_post = id_producto_diferenciado
    else:
        id_producto_post = id_producto_regular

    if 'autonomo' in request.POST:
        autonomo_post = 1
    else:
        autonomo_post = 0

    objAlumno = TblAlumnos.objects.filter(rut_alumno=str(rut))

    if objAlumno:
        if objAlumno[0].autonomo==1:
            autonomo_post = 1

        try:
            objAlumno.update(nombre=nombre, apellido=apellido, autonomo=autonomo_post, id_producto=id_producto_post)
        except:
            responde['estatus'] = 0
            responde['mensaje'] = 'Ocurrio un error, intente nuevamente.'

        objContenidoUnidadActual= TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad', 'orden')
        for contenidoUnidad in objContenidoUnidadActual:
            try:
                TblPlanAutonomo(rut_alumno=TblAlumnos.objects.get(rut_alumno=str(rut)), id_contenido=TblContenidos.objects.get(id_contenido=contenidoUnidad.id_contenido.id_contenido), id_unidad=TblUnidades.objects.get(id_unidad=contenidoUnidad.id_unidad.id_unidad),fecha_registro= fecha_registro, orden=contenidoUnidad.orden).save()
            except:
                responde['estatus'] = 0
                responde['mensaje'] = 'Ocurrio un error, intente nuevamente.'
    else:
        responde['estatus'] = 0
        responde['mensaje'] = 'Ocurrio un error, intente nuevamente.'

    return HttpResponse(json.dumps(responde))

def verificarAlumno(request):
    rut = request.POST['rutAlumno']
    responde = {'estatus': 1, 'mensaje': ''}
    id_producto_diferenciado = 3
    id_producto_regular = 2

    if 'id_producto' in request.POST:
        id_producto_post = id_producto_diferenciado
    else:
        id_producto_post = id_producto_regular

    if 'autonomo' in request.POST:
        autonomo_post = 1
    else:
        autonomo_post = 0

    objAlumno = TblAlumnos.objects.filter(rut_alumno=str(rut))

    if objAlumno:

        if int(objAlumno[0].id_producto.id_producto) != int(id_producto_post) or int(objAlumno[0].autonomo) != int(
                autonomo_post):
            if int(autonomo_post) == 1:
                responde['estatus'] = 2
                responde['mensaje'] = 'Otorgado la modalidad de trabajo autonomo.'
            elif int(id_producto_post) == id_producto_diferenciado:
                responde['estatus'] = 3
                responde['mensaje'] = 'Otorgado el plan de trabajo diferenciado.'
            elif int(id_producto_post) == 0:
                responde['estatus'] = 1
            elif int(objAlumno[0].autonomo) == 1:
                responde['estatus'] = 1
            elif int(id_producto_post) != id_producto_diferenciado:
                responde['estatus'] = 4
                responde['mensaje'] = 'Remocion trabajo diferenciado.'
    else:
        responde['estatus'] = 0
        responde['mensaje'] = 'Ocurrio un error, intente nuevamente.'

    return HttpResponse(json.dumps(responde))

def consultarAlumno(request):
    rut = request.POST['rut']
    response = {}
    objAlumno = TblAlumnos.objects.filter(rut_alumno=str(rut))
    if objAlumno:
        response['rut_alumno'] = objAlumno[0].rut_alumno
        response['nombre'] = objAlumno[0].nombre
        response['apellido'] = objAlumno[0].apellido
        response['id_producto'] = objAlumno[0].id_producto.id_producto
        response['autonomo'] = objAlumno[0].autonomo

    return HttpResponse(json.dumps(response))

def listarAlumnosPorLista(request):
    codLista = request.session['curso']
    data = []
    objAlumnos = TblAlumnos.objects.filter(codigo_lista=TblListas.objects.get(codigo_lista=codLista), activo=1).order_by('apellido')
    indice = 0
    listaActual= TblListas.objects.filter(codigo_lista=codLista)

    # Se verifica si la la activacion esta de 1-1 o todas activas
    if listaActual[0].id_producto.id_producto == 3:
        for alumno in objAlumnos:
            indice += 1
            if listaActual[0].activar_unidades == 0:
                diferenciado = '<div class="bg-naranjo"><li class="fas fa-check"></li></div>' if alumno.id_producto.id_producto == 3 else ''
                data.append(
                    [indice,
                     str(alumno.apellido) +' '+ str(alumno.nombre),
                     alumno.rut_alumno,
                     alumno.clave,
                     alumno.respuesta,
                     diferenciado,
                     '<a href="#" onclick="consultarAlumno(\'' + str(
                         alumno.rut_alumno) + '\',event)" class="btn btn-info  btn-icon-split btn-sm"><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Editar</span></a>'
                     ])
            else:
                autonomo = '<div class="bg-naranjo"><li class="fas fa-check"></li></div>' if alumno.autonomo == 1 else ''
                diferenciado = '<div class="bg-naranjo"><li class="fas fa-check"></li></div>' if alumno.id_producto.id_producto == 3 else ''
                data.append(
                    [indice,
                     str(alumno.apellido) +' '+ str(alumno.nombre),
                     alumno.rut_alumno,
                     alumno.clave,
                     alumno.respuesta,
                     diferenciado,
                     autonomo,
                     '<a href="#" onclick="consultarAlumno(\'' + str(
                         alumno.rut_alumno) + '\',event)" class="btn btn-info  btn-icon-split btn-sm"><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Editar</span></a>'
                     ])




        response = {'sEcho': 1, 'iTotalRecords': len(data), 'iTotalDisplayRecords': len(data), 'aaData': data}
    else:
        for alumno in objAlumnos:
            indice += 1
            if listaActual[0].activar_unidades == 0:
                data.append(
                    [indice,
                     str(alumno.apellido) +' '+ str(alumno.nombre),
                     alumno.rut_alumno,
                     alumno.clave,
                     alumno.respuesta,
                     '<a href="#" onclick="consultarAlumno(\'' + str(
                         alumno.rut_alumno) + '\',event)" class="btn btn-info  btn-icon-split btn-sm"><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Editar</span></a>'
                     ])
            else:
                autonomo = '<div class="bg-naranjo"><li class="fas fa-check"></li></div>' if alumno.autonomo == 1 else ''
                data.append(
                    [indice,
                     str(alumno.apellido) +' '+ str(alumno.nombre),
                     alumno.rut_alumno,
                     alumno.clave,
                     alumno.respuesta,
                     autonomo,
                     '<a href="#" onclick="consultarAlumno(\'' + str(
                         alumno.rut_alumno) + '\',event)" class="btn btn-info  btn-icon-split btn-sm"><span class="icon text-white-50"><i class="fas fa-edit"></i></span><span class="text">Editar</span></a>'
                     ])

        response = {'sEcho': 1, 'iTotalRecords': len(data), 'iTotalDisplayRecords': len(data), 'aaData': data}


    return HttpResponse(json.dumps(response))

def ordenContenido(request):
    if request.session.get("rut", False):
        rut = request.session['rut']
    else:
        return redirect('/ggtutbas')

    fullName = request.session['fullName']
    colegio = request.session['nombreColegio']

    if 'codLista' in request.GET:
        codLista = request.GET['codLista']
        request.session['curso'] = codLista
    else:
        codLista = request.session['curso']


    unidad= {}
    contUnidades=[]

    nivel = TblListas.objects.get(codigo_lista=codLista)
    contenidoUnidades= TblContenidoUnidad.objects.filter(codigo_lista=codLista).order_by('id_unidad', 'orden')
    ##contenidoUnidades= TblContenidoUnidad.objects.select_related('id_contenido','id_unidad').filter(codigo_lista=codLista).order_by('orden')

    for contenidoUnidad in contenidoUnidades:
        unidad={'id_unidad': contenidoUnidad.id_unidad.id_unidad,'nombre_unidad': contenidoUnidad.id_unidad.nombre_unidad, 'id_contenido':contenidoUnidad.id_contenido.id_contenido, 'descripcion':contenidoUnidad.id_contenido.descripcion,'orden':contenidoUnidad.orden}
        contUnidades.append(unidad)
    variables = variablesPais(request)

    data = {
        'rut': rut,
        'fullName': fullName,
        'codLista': codLista,
        'nivel': nivel.id_nivel,
        'contUnidades':contUnidades,
        'nombreColegio': colegio,
        'variables': variables,

    }

    return render(request, 'ggtutbas/plan_orden_contenido.html', data)

def editarPosicion(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
    else:
        return redirect('/ggtutbas')
    fullName = request.session['fullName']
    codLista = request.session['curso']
    colegio = request.session['nombreColegio']
    unidad= {}
    contUnidades=[]

    nivel = TblListas.objects.get(codigo_lista=codLista)
    contenidoUnidades= TblContenidoUnidad.objects.filter(codigo_lista=codLista).order_by('id_unidad', 'orden')
    ##contenidoUnidades= TblContenidoUnidad.objects.select_related('id_contenido','id_unidad').filter(codigo_lista=codLista).order_by('orden')

    for contenidoUnidad in contenidoUnidades:
        plan = TblPlan.objects.filter(id_contenido_unidad=contenidoUnidad.id_contenido_unidad)
        if plan:
            clase= 'ui-state-disabled'
        else:
            clase= 'none'
        unidad={'id_unidad': contenidoUnidad.id_unidad.id_unidad,'nombre_unidad': contenidoUnidad.id_unidad.nombre_unidad, 'id_contenido':contenidoUnidad.id_contenido.id_contenido, 'descripcion':contenidoUnidad.id_contenido.descripcion,'orden':contenidoUnidad.orden, 'class': clase}
        contUnidades.append(unidad)

    variables = variablesPais(request)

    data = {
        'rut': rut,
        'fullName': fullName,
        'codLista': codLista,
        'nivel': nivel.id_nivel,
        'contUnidades':contUnidades,
        'nombreColegio': colegio,
        'variables': variables,

    }

    return render(request, 'ggtutbas/plan_organizacion_contenido.html', data)

def ordenPosicion(request):
    codLista = request.session['curso']
    posiciones= request.POST.getlist('positions[]')
    lista_posiciones= json.loads(posiciones[0])
    respuesta={}
    contador=0
    listaCont= []
    contUnidades = []



    for posicion in lista_posiciones:
        contenido=posicion[0]
        unidad=posicion[1]
        orden=posicion[2]
        contador+=1


        objContenidoUnidad=TblContenidoUnidad.objects.filter(id_contenido=TblContenidos.objects.get(id_contenido=contenido), codigo_lista=codLista)

        listaCont.append(objContenidoUnidad[0].id_contenido_unidad)

        plan = TblPlan.objects.filter(id_contenido_unidad=objContenidoUnidad[0])
        if plan:
            respuesta['plan'] = False
            break
        else:
            respuesta['plan']= True
    if respuesta['plan']:
        for posicion in lista_posiciones:
            contenido = posicion[0]
            unidad = posicion[1]
            orden = posicion[2]

            objUnidadActiva = TblContenidoUnidad.objects.filter(id_unidad=TblUnidades.objects.get(id_unidad=unidad), codigo_lista=codLista)
            if objUnidadActiva:
                if objUnidadActiva[0].activo==1:
                    activo=1
                    fecha=objUnidadActiva[0].fecha_modificacion
                else:
                    activo=0
                    fecha=None
                unidad = {'codLista': codLista,
                          'id_contenido': contenido,
                          'id_unidad': unidad,
                          'orden': orden,
                          'activo': activo,
                          'fecha': fecha}
                contUnidades.append(unidad)
            else:
                respuesta['plan'] = False

        for contUnidad in contUnidades:
            try:
                TblContenidoUnidad.objects.filter(
                        codigo_lista=TblListas.objects.get(codigo_lista=contUnidad['codLista']),
                        id_contenido=TblContenidos.objects.get(
                            id_contenido=contUnidad['id_contenido'])).update(id_unidad=contUnidad['id_unidad'],
                                                                       orden=int(contUnidad['orden']),
                                                                       activo=int(contUnidad['activo']), fecha_modificacion=fecha)
                respuesta['status'] = 'ok'
            except:
                respuesta['status'] = 'error'


    respuesta['contador'] = contador
    respuesta['lista-contenido']= listaCont


    response = json.dumps(respuesta)

    return HttpResponse(response)

class Pdf(View):

    def get(self, request):
        if request.session.get("rut", False):
            rut = request.session['rut']
            rbd = request.session['rbd']
        else:
            return redirect('/ggtutbas')
        codLista = request.session['curso']
        datosAlumnos= TblAlumnos.objects.filter(codigo_lista=codLista)
        colegio= TblInstituciones.objects.get(rbd=rbd)
        nivel = TblListas.objects.get(codigo_lista=codLista)
        curso= str(nivel.id_nivel)+' básico '+str(nivel.letra)
        data = {
            'request': request,
            'alumnos': datosAlumnos,
            'curso': curso,
            'colegio': colegio
        }
        return Render.render('ggtutbas/credencialesAlumnos.html', data)

def activarUnidades(request):

    if request.session.get("rut", False):
        rut = request.session['rut']
        rbd = request.session['rbd']
    else:
        return redirect('/ggtutbas')

    fullName = request.session['fullName']
    colegio = request.session['nombreColegio']

    if 'codLista' in request.GET:
        codLista = request.GET['codLista']
        request.session['curso'] = codLista
    else:
        codLista = request.session['curso']


    modoActivar = TblListas.objects.filter(codigo_lista=codLista)

    if modoActivar[0].activar_unidades==1:
        parrafo= 'Actualmente el programa tiene habilitada la opción activación de unidades una a una, por lo que debes activar cada unidad consecutivamente para que los alumnos puedan trabajar'
        modal='(leer instructivo).'
        contParrafo='La primera unidad ya se encuentra activada.'
        modalidad= 'Activar todas las unidades'
        mensajeActivacion='Has activado todas las unidades permitiendo que los estudiantes avancen a su ritmo por todas las actividades del programa EMAT. ¿Estás seguro de este cambio?'
    else:
        parrafo= 'Actualmente el programa tiene habilitada la opción “todas las unidades activadas”,'
        modal=''
        contParrafo=''
        modalidad= 'Activar unidades una a una'
        mensajeActivacion='Has optado por activar una a una las unidades del programa, donde el plan de trabajo del alumno estará disponible hasta la última unidad que actives. ¿Estás seguro de este cambio?'

    contenidoUnidades= TblContenidoUnidad.objects.filter(codigo_lista= codLista).order_by('id_unidad', 'orden')

    variables = variablesPais(request)

    data = {
        'rut': rut,
        'fullName': fullName,
        'codLista': codLista,
        'nombreColegio': colegio,
        'contenidoUnidades':contenidoUnidades,
        'parrafo': parrafo,
        'modal': modal,
        'contParrafo': contParrafo,
        'modalidad': modalidad,
        'tipo': modoActivar[0].activar_unidades,
        'mensajeActivacion': mensajeActivacion,
        'variables': variables,

    }
    ##return HttpResponse(contenidoUnidades)
    return render(request, 'ggtutbas/plan_activar_unidades.html', data)

def activaUnidad(request):
    idUnidad= request.POST['idUnidad']
    contenidoUnidad = TblContenidoUnidad.objects.filter(id_contenido_unidad=idUnidad)

    respuesta={}
    now = datetime.datetime.now()
    fecha_registro = now.strftime("%Y-%m-%d %H:%M:%S")



    if contenidoUnidad:
        contenidos = TblContenidoUnidad.objects.filter(id_unidad=contenidoUnidad[0].id_unidad,codigo_lista=contenidoUnidad[0].codigo_lista)

        for contenido in contenidos:
            try:
                TblContenidoUnidad.objects.filter(id_contenido_unidad=contenido.id_contenido_unidad).update(activo=1, fecha_modificacion=fecha_registro)
                respuesta['contenido']='ok'

            except:
                respuesta['contenido'] = 0
                respuesta['mensaje'] = 'Ocurrio un error, intente nuevamente.'

    responde = json.dumps(respuesta)

    return HttpResponse(responde)


def cambiarModoActiva(resquest):
    activarUnidades = resquest.POST['tipo']
    lista=resquest.POST['lista']
    contenidos = TblContenidoUnidad.objects.filter(codigo_lista=lista).order_by('id_unidad', 'orden')
    unidad={}
    respuesta={}
    contUnidades=[]
    now = datetime.datetime.now()
    fecha_registro = now.strftime("%Y-%m-%d %H:%M:%S")


    if int(activarUnidades)== 0:
        activo= 1
        contenidosUnidades=TblContenidoUnidad.objects.filter(codigo_lista=lista).order_by('id_unidad', 'orden')
        primeraFecha= contenidosUnidades[0].fecha_modificacion
        for contenido in contenidosUnidades:
            plan= TblPlan.objects.filter(id_contenido_unidad= contenido.id_contenido_unidad)
            if plan:
                TblContenidoUnidad.objects.filter(id_contenido_unidad= contenido.id_contenido_unidad, codigo_lista=lista).update(activo=1, fecha_modificacion=contenido.fecha_modificacion)
                unidad={'plan':contenido.id_contenido_unidad, 'activos':contenido.id_unidad.id_unidad}
            else:
                TblContenidoUnidad.objects.filter(id_contenido_unidad= contenido.id_contenido_unidad, codigo_lista=lista).update(activo=0, fecha_modificacion=None)
                unidad={'plan':contenido.id_contenido_unidad, 'no-activos':contenido.id_unidad.id_unidad}
            contUnidades.append(unidad)
        ##return HttpResponse(contUnidades)
        TblContenidoUnidad.objects.filter(id_unidad=contenidos[0].id_unidad.id_unidad).order_by('id_unidad','orden').update(activo=1, fecha_modificacion=primeraFecha)
        ##return HttpResponse(contUnidades)

    else:
        activo = 0

        for contenido in contenidos:

            if contenido.fecha_modificacion:
                TblContenidoUnidad.objects.filter(codigo_lista=lista, id_unidad=contenido.id_unidad.id_unidad).update(activo=1, fecha_modificacion=contenido.fecha_modificacion)

            else:
               TblContenidoUnidad.objects.filter(codigo_lista=lista, id_unidad=contenido.id_unidad.id_unidad).update(activo=1, fecha_modificacion=fecha_registro)

        TblContenidoUnidad.objects.filter(id_unidad=contenidos[0].id_unidad.id_unidad).order_by('id_unidad', 'orden').update(activo=1)
    respuesta['activacion']=True
    TblListas.objects.filter(codigo_lista=lista).update(activar_unidades=activo)

    responde = json.dumps(respuesta)

    return HttpResponse(responde)

def manualUsuario(request):

    if request.session.get("rut", False):
        colegio = request.session['nombreColegio']
        rut = request.session['rut']
    elif 'rut' in request.GET:
        rut = request.GET['rut']
        colegio = 'nombre del colegio'
    else:
        return redirect('/ggtutbas')

    if request.session.get("fullName", False):
        fullName = request.session['fullName']
    else:
        fullName = request.GET['fullName']

    if 'codLista' in request.GET:
        codLista = request.GET['codLista']
        request.session['curso'] = codLista
    elif request.session.get("curso", False):
        codLista = request.session['curso']
    else:
        codLista = ''

    rbd = request.session['rbd']

    cantidadListasDiferenciadas = 0
    listasTutor = TblListas.objects.filter(rut_tutor__rut_tutor=rut, rbd__rbd=rbd)
    for objTblListas in listasTutor:
        if int(objTblListas.id_producto.id_producto) == 3:
            cantidadListasDiferenciadas += 1
    variables = variablesPais(request)

    data = {
        'fullName': fullName,
        'nombreColegio': colegio,
        'codLista': codLista,
        'cantidadListasDiferenciadas': cantidadListasDiferenciadas,
        'variables': variables,
    }

    return render(request, 'ggtutbas/manualUsuario.html', data)





