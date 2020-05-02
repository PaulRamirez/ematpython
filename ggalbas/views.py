import json
import random
import string
import datetime
import base64
import socket
from datetime import date
import math
import locale
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import register
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Count, Min, Sum
from ggalbas.models import TblAlumnos, TblListas, TblPreguntausuarios, TblSubproducto, TblRegistroipAlumno, TblNiveles, \
    TblInstituciones, TblActividades, TblTipoActividad, TblAlumnoActividades, TblAlumnoRespuestas, TblPreguntas, \
    TblHabilidades, TblEje, TblAlumnoDiagnostico, TblContenidoUnidad, TblPlanAutonomo, TblUnidades, TblContenidosFasesActividades, \
    TblContenidos, TblFases, TblPlan
from core.models import Preguntas2Basico, Pruebas, PreguntasInstancias
from core.views import flagPais

def variablesPais(request):
    pais=flagPais(request)
    #declaracion de variables de acuerdo a pais, por defecto se setea CL
    if str(pais)=='pe':
        rut= 'Id usuario'
        curso='Sección'
        niveles = TblNiveles.objects.filter(categoria='BP')
    elif str(pais)=='cl':
        rut= 'Rut'
        curso='Curso'
        niveles = TblNiveles.objects.filter(categoria='B')
    else:
        rut= 'Rut'
        curso='Curso'
        niveles = TblNiveles.objects.filter(categoria='B')

    data={
        'rut':rut,
        'curso':curso,
        'niveles': niveles,
        'pais': pais,
    }

    return (data)


def index(request):
    variables=variablesPais(request)
    captcha = random.randrange(1000, 9999)

    data={
        'variables':variables,
        'captcha':captcha,
    }

    return render(request, 'ggalbas/login.html', data)

def nuevoAlumno(request):
    variables=variablesPais(request)

    data={
        'variables':variables,
    }
    return render(request, 'ggalbas/nuevoAlumno.html', data)

def agregarAlumno(request):
    rut = request.POST['rut']
    nombres = request.POST['nombres'].upper()
    apellidos = request.POST['apellidos'].upper()
    pregunta = TblPreguntausuarios.objects.get(id_pregunta=int(request.POST['pregunta']))
    producto = TblSubproducto.objects.get(id_producto=2)
    answer = request.POST['respuesta'].upper()
    nivel = TblNiveles.objects.get(id_nivel=int(request.POST['curso']))
    letra = request.POST['letra'].upper()
    codigoLista = request.POST['codigoLista'].upper()
    #caracteres = string.ascii_letters + string.digits
    #password = ''.join(random.choice(caracteres) for _ in range(6))
    password= random.randrange(1000, 9999)
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")
    respuesta = {}

    ##se consulta si el rut ingresado pertenece a algun alumno
    consulta = TblAlumnos.objects.filter(rut_alumno=rut)

    if consulta:
        respuesta['alumno'] = 'alumno existe'
    else:
        ##se consulta que la lista este asociada al nivel

        consultaLista = TblListas.objects.filter(codigo_lista=codigoLista, id_nivel=nivel, letra=letra)


        if consultaLista:
            try:
                tutor = consultaLista[0].rut_tutor.rut_tutor
            except ObjectDoesNotExist:
                tutor = False
            if tutor:
                respuesta['lista'] = 'ok'
                ## consulta de cupos disponibles
                if consultaLista[0].total_alumnos == consultaLista[0].alumnos_registrados:
                    respuesta['cupo'] = False
                else:
                    try:
                        consultaLista.update(alumnos_registrados=int(consultaLista[0].alumnos_registrados) + 1)
                        respuesta['cupo'] = True
                    except:
                        respuesta['status'] = 'error al guardar'
                    registroAlumno = TblAlumnos(rut_alumno=rut, nombre=nombres, apellido=apellidos, clave=password,
                                                id_pregunta=pregunta, respuesta=answer,
                                                id_producto=producto, activo=1, nuevo=1, autonomo=0,
                                                fecha_registro=fechaActual,
                                                codigo_lista=TblListas.objects.get(codigo_lista=str(codigoLista)), libre=0)

                    try:
                        registroAlumno.save()
                        respuesta['alumno'] = 'ok'
                        alumnoRegistrado = TblAlumnos.objects.filter(rut_alumno=rut)
                        respuesta['password'] = alumnoRegistrado[0].clave
                    except:
                        respuesta['status'] = 'error al guardar'


            else:
                respuesta['tutor'] = 'no'
        else:
            respuesta['lista'] = 'error'

    responde = json.dumps(respuesta)
    return HttpResponse(responde)

def recuperaClave(request):
    variables=variablesPais(request)

    data={
        'variables':variables,
    }
    return render(request, 'ggalbas/recuperaClave.html', data)

def verificaRut(request):
    rut = request.POST['rut']
    consulta = TblAlumnos.objects.filter(rut_alumno=rut)
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
    consulta = TblAlumnos.objects.filter(rut_alumno=rut, respuesta=answer.upper())
    respuesta = {}
    if consulta:
        respuesta['status'] = 'respuesta ok'
        respuesta['password'] = consulta[0].clave
    else:
        respuesta['status'] = 'error'
    responde = json.dumps(respuesta)
    return HttpResponse(responde)

def verificaRutIp(request):
    rut = request.POST['rut']
    ip = request.POST['ip']
    respuesta = {}

    consulta = TblRegistroipAlumno.objects.filter(rut_alumno=rut, ip=ip)

    if consulta:
        respuesta['status'] = 'validado'
    else:
        respuesta['status'] = 'sin datos'

    responde = json.dumps(respuesta)

    return HttpResponse(responde)

def ingresoCompleto(request):

    rut = request.POST['rut']
    password = request.POST['password']
    ip = request.POST['ip']

    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")
    hoy = date.today()
    year = format(hoy.year)

    fecha = datetime.date(int(year), 7, 31)
    primerLunesAgosto = proximo_dia_semana(fecha, 0)  # 0 = lunes, 1=martes, 2=miercoles...


    fecha = datetime.date(int(year), 10, 31)
    primerLunesNoviembre = proximo_dia_semana(fecha, 0)  # 0 = lunes, 1=martes, 2=miercoles...


    respuesta = {'estatus': 1, 'mensaje': ''}

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut, clave__regex=password, id_producto__id_producto__in=(2, 3))

    if objAlumno:

        #  guarda la ip del alumno.
        registro = TblRegistroipAlumno(rut_alumno=TblAlumnos.objects.get(rut_alumno=rut), ip=ip, fecha_registro=fechaActual)
        try:
            registro.save()
        except:
            respuesta = {'estatus': 0, 'mensaje': 'error de conexion.'}

        # Declaracion de las variables de session
        request.session['rut'] = objAlumno[0].rut_alumno
        request.session['nombres'] = objAlumno[0].nombre + ' ' + objAlumno[0].apellido
        request.session['id_nivel'] = int(objAlumno[0].codigo_lista.id_nivel.id_nivel)
        request.session['numero_nivel'] = int(objAlumno[0].codigo_lista.id_nivel.numero_nivel)
        request.session['nivel'] = str(objAlumno[0].codigo_lista.id_nivel.nivel) + '-' + str(objAlumno[0].codigo_lista.letra)
        request.session['rbd'] = str(objAlumno[0].codigo_lista.rbd.nombre_institucion)

        siglasIniciales = ''
        pais = flagPais(request)

        if pais == 'cl':
            siglasIniciales = 'P'
        if pais == 'pe':
            siglasIniciales = 'PP'

        nombreDiagnosticoInicial = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GG' + '01' + year
        nombreDiagnosticoInicialDiferenciado = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GD' + '01' + year

        request.session['prueba'] = nombreDiagnosticoInicial
        request.session['prueba_diferenciada'] = nombreDiagnosticoInicialDiferenciado

        nombreDiagnosticoIntermedio = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GG' + '02' + year
        nombreDiagnosticoIntermedioDiferenciado = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GD' + '02' + year

        nombreDiagnosticoFinal = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GG' + '03' + year
        nombreDiagnosticoFinalDiferenciado = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GD' + '03' + year

        url_alumno = ''

        if int(objAlumno[0].nuevo) == 1:
            url_alumno = 'antePortada'

        if int(objAlumno[0].nuevo) == 0 and int(objAlumno[0].libre) == 0:
            url_alumno = 'unidadesAlumno'

        if int(objAlumno[0].nuevo) == 0 and int(objAlumno[0].libre) == 1:
            url_alumno = 'complementariasLibre'

        listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).order_by('fecha_inicio')

        if listaObjAlumnoActividades:

            objUltimaActividadAlumno = listaObjAlumnoActividades.last()

            if objUltimaActividadAlumno.fecha_fin is None and objUltimaActividadAlumno.puntaje is None:

                if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) in [5, 6, 7] and int(objAlumno[0].libre) == 0:
                    url_alumno = 'complementariasUnidad'

                if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) in [5, 6, 7] and int(objAlumno[0].libre) == 1:
                    url_alumno = 'complementariasLibre'

                if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 1:
                    request.session['prueba'] = str(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad)
                    url_alumno = 'antePortada'

        # buscar la fecha del primer Diagnostico Inicial finalizado por la lista del Estudiante.
        result = TblAlumnoActividades.objects.filter(rut_alumno__codigo_lista=objAlumno[0].codigo_lista, id_contenido_fase_actividad__id_actividad__nombre_actividad=nombreDiagnosticoInicial).aggregate(fecha_primer_diagnostico=Min('fecha_fin'))

        if result['fecha_primer_diagnostico'] is None:
            dias_desde_primer_diagnostico = 0
        else:
            dias_desde_primer_diagnostico = int((now - result['fecha_primer_diagnostico']).days)

        # Activacion del Diagnostico Intermedio.
        if hoy >= primerLunesAgosto:

            existePruebaIntermedia = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_actividad__nombre_actividad=nombreDiagnosticoIntermedio).count()

            if int(objAlumno[0].codigo_lista.prueba_intermedia) == 1 and dias_desde_primer_diagnostico >= 90 and existePruebaIntermedia == 0:
                request.session['prueba'] = nombreDiagnosticoIntermedio
                request.session['prueba_diferenciada'] = nombreDiagnosticoIntermedioDiferenciado
                url_alumno = 'antePortada'

        # Activacion del Diagnostico Final.
        if hoy >= primerLunesNoviembre:

            existePruebaFinal = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_actividad__nombre_actividad=nombreDiagnosticoFinal).count()

            if dias_desde_primer_diagnostico >= 60 and existePruebaFinal == 0:
                request.session['prueba'] = nombreDiagnosticoFinal
                request.session['prueba_diferenciada'] = nombreDiagnosticoFinalDiferenciado
                url_alumno = 'antePortada'

        respuesta['url_alumno'] = url_alumno

    else:
        respuesta = {'estatus': 0, 'mensaje': 'El rut y/o contraseña ingresados no son válidos'}
    # end if.

    responde = json.dumps(respuesta)

    return HttpResponse(responde)

def ingresoSoloRut(request):

    respuesta = {'estatus': 1, 'mensaje': ''}
    rut = request.POST['rut']

    hoy = date.today()
    year = format(hoy.year)
    now = datetime.datetime.now()

    fecha = datetime.date(int(year), 7, 31)
    primerLunesAgosto = proximo_dia_semana(fecha, 0)  # 0 = lunes, 1=martes, 2=miercoles...


    fecha = datetime.date(int(year), 10, 31)
    primerLunesNoviembre = proximo_dia_semana(fecha, 0)  # 0 = lunes, 1=martes, 2=miercoles...


    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut, activo=1, id_producto__id_producto__in=(2, 3))

    if objAlumno:

        # Declaracion de las variables de session
        request.session['rut'] = objAlumno[0].rut_alumno
        request.session['nombres'] = objAlumno[0].nombre + ' ' + objAlumno[0].apellido
        request.session['id_nivel'] = int(objAlumno[0].codigo_lista.id_nivel.id_nivel)
        request.session['numero_nivel'] = int(objAlumno[0].codigo_lista.id_nivel.numero_nivel)
        request.session['nivel'] = str(objAlumno[0].codigo_lista.id_nivel.nivel) + '-' + str(objAlumno[0].codigo_lista.letra)
        request.session['rbd'] = str(objAlumno[0].codigo_lista.rbd.nombre_institucion)

        siglasIniciales = ''
        pais = flagPais(request)

        if pais == 'cl':
            siglasIniciales = 'P'
        if pais == 'pe':
            siglasIniciales = 'PP'

        nombreDiagnosticoInicial = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GG' + '01' + year
        nombreDiagnosticoInicialDiferenciado = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GD' + '01' + year

        request.session['prueba'] = nombreDiagnosticoInicial
        request.session['prueba_diferenciada'] = nombreDiagnosticoInicialDiferenciado

        nombreDiagnosticoIntermedio = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GG' + '02' + year
        nombreDiagnosticoIntermedioDiferenciado = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GD' + '02' + year

        nombreDiagnosticoFinal = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GG' + '03' + year
        nombreDiagnosticoFinalDiferenciado = siglasIniciales + str(objAlumno[0].codigo_lista.id_nivel.numero_nivel) + 'GD' + '03' + year

        url_alumno = ''

        if int(objAlumno[0].nuevo) == 1:    # redirecciona al diagnostico.
            url_alumno = 'antePortada'

        if int(objAlumno[0].nuevo) == 0 and int(objAlumno[0].libre) == 0:
            url_alumno = 'unidadesAlumno'

        if int(objAlumno[0].nuevo) == 0 and int(objAlumno[0].libre) == 1:
            url_alumno = 'complementariasLibre'

        listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).order_by('fecha_inicio')

        if listaObjAlumnoActividades:

            objUltimaActividadAlumno = listaObjAlumnoActividades.last()

            if objUltimaActividadAlumno.fecha_fin is None and objUltimaActividadAlumno.puntaje is None:

                if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) in [5, 6, 7] and int(objAlumno[0].libre) == 0:
                    url_alumno = 'complementariasUnidad'

                if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) in [5, 6, 7] and int(objAlumno[0].libre) == 1:
                    url_alumno = 'complementariasLibre'

                if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 1:
                    request.session['prueba'] = str(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad)
                    url_alumno = 'antePortada'

        # buscar la fecha del primer Diagnostico Inicial finalizado por la lista del Estudiante.
        result = TblAlumnoActividades.objects.filter(rut_alumno__codigo_lista=objAlumno[0].codigo_lista, id_contenido_fase_actividad__id_actividad__nombre_actividad=nombreDiagnosticoInicial).aggregate(fecha_primer_diagnostico=Min('fecha_fin'))

        if result['fecha_primer_diagnostico'] is None:
            dias_desde_primer_diagnostico = 0
        else:
            dias_desde_primer_diagnostico = (now - result['fecha_primer_diagnostico']).days

        # Activacion del Diagnostico intermedio.
        if hoy >= primerLunesAgosto:

            existePruebaIntermedia = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_actividad__nombre_actividad=nombreDiagnosticoIntermedio).count()

            if int(objAlumno[0].codigo_lista.prueba_intermedia) == 1 and dias_desde_primer_diagnostico >= 90 and existePruebaIntermedia == 0:
                request.session['prueba'] = nombreDiagnosticoIntermedio
                request.session['prueba_diferenciada'] = nombreDiagnosticoIntermedioDiferenciado
                url_alumno = 'antePortada'

        # Activacion del Diagnostico Final.
        if hoy >= primerLunesNoviembre:

            existePruebaFinal = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_actividad__nombre_actividad=nombreDiagnosticoFinal).count()

            if dias_desde_primer_diagnostico >= 60 and existePruebaFinal == 0:
                request.session['prueba'] = nombreDiagnosticoFinal
                request.session['prueba_diferenciada'] = nombreDiagnosticoFinalDiferenciado
                url_alumno = 'antePortada'

        respuesta['url_alumno'] = url_alumno

    else:
        respuesta = {'estatus': 0, 'mensaje': 'error al consultar el rut del alumno.'}


    responde = json.dumps(respuesta)

    return HttpResponse(responde)

def antePortada(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    return render(request, 'ggalbas/antePortada.html')

def portadaVisor(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    prueba = request.session['prueba']

    consultaActividad = Pruebas.objects.using('e_test').filter(codprueba=prueba)

    if consultaActividad:
        # # se guarda en una variable de sesion el id de la prueba o guia que corresponda
        request.session['prueba_guia'] = consultaActividad[0].idprueba
        descripcion = consultaActividad[0].descprueba
    else:
        descripcion = 'no se encontro la prueba diagnostico.'

    data = {
            'descripcion': descripcion,
            }

    return render(request, 'ggalbas/portadaVisor.html', data)

def visorActividades(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    hoy = date.today()
    year = format(hoy.year)
    id_nivel = request.session['id_nivel']
    pruebaGuia = request.session['prueba_guia']
    prueba = request.session['prueba']
    prueba_diferenciada = request.session['prueba_diferenciada']
    bd = 'e_test'
    pais = flagPais(request)

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)
    numero_nivel = int(objAlumno[0].codigo_lista.id_nivel.numero_nivel)

    # verificar que existe la prueba diagnostico en tabla actividades.
    actividad = TblActividades.objects.filter(prueba_guia=pruebaGuia)

    if actividad:
        descripcion = actividad[0].descripcion_actividades
    else:

        # consultar actividad diagnostico en base de datos e_test
        objPrueba = Pruebas.objects.using('e_test').filter(codprueba=prueba, idprueba=pruebaGuia)

        if objPrueba:

            descripcion = objPrueba[0].descprueba
            # crear la actividad Guiada.
            objTipoActividad = TblTipoActividad.objects.filter(id_tipo_actividad=1)
            actividadGuiada = TblActividades(nombre_actividad=prueba, descripcion_actividades=objPrueba[0].descprueba, id_tipo_actividad=objTipoActividad[0], npreguntas=objPrueba[0].npreguntas, prueba_guia=pruebaGuia)
            actividadGuiada.save()

            # crea registro en tabla tbl_contenido_fase_actividad para la actividad de diagnostico guiado.
            objFase = TblFases.objects.filter(id_fase=1)

            objContenidoFaseActividadGuiado = TblContenidosFasesActividades(id_fase=objFase[0], id_actividad=actividadGuiada, orden=1)
            objContenidoFaseActividadGuiado.save()

            # crear la actividad Diferenciada.
            id_padre = int(actividadGuiada.id_actividad)
            actividadDiferenciada = TblActividades(nombre_actividad=prueba_diferenciada, descripcion_actividades=objPrueba[0].descprueba, id_tipo_actividad=objTipoActividad[0], npreguntas=objPrueba[0].npreguntas, prueba_guia=pruebaGuia, id_padre=id_padre)
            actividadDiferenciada.save()

            # crea registro en tabla tbl_contenido_fase_actividad
            objContenidoFaseActividadDiferenciado = TblContenidosFasesActividades(id_fase=objFase[0], id_actividad=actividadDiferenciada, orden=1)
            objContenidoFaseActividadDiferenciado.save()


        else:
            descripcion = 'no se encontro la actividad en base de datos e_test.'
        # end if.
    # end if.

    # consulta las preguntas en base de datos e-test.
    listaPreguntas2Basico = Preguntas2Basico.objects.using(bd).filter(idprueba=pruebaGuia)
    total_ejercicios = len(listaPreguntas2Basico)

    # consulta las respuestas del alumno.
    listaTblAlumnoRespuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=rut_alumno, prueba_guia=pruebaGuia)

    if listaTblAlumnoRespuestas:
        npregunta = int(listaTblAlumnoRespuestas.last().npregunta)
    else:
        npregunta = 0

    if npregunta == total_ejercicios:
        return redirect('portadaFinalDiagnostico')

    imagen_ejercicio = base64.b64encode(listaPreguntas2Basico[npregunta].imagen).decode()
    posiciones = str(listaPreguntas2Basico[npregunta].posiciones_botones)
    pos_boton = posiciones.replace('!', "")
    lista_pos = pos_boton.split(',')
    posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]

    npreg = listaPreguntas2Basico[npregunta].npregunta
    tipo_ejercicio = listaPreguntas2Basico[npregunta].tipo_ejercicio

    siglasIniciales = ''

    if pais == 'cl':
        siglasIniciales = 'p'

    if pais == 'pe':
        siglasIniciales = 'pp'

    audio_pregunta = 'e_test/' + siglasIniciales + str(numero_nivel) + '01' + str(year) + '_e' + str(npreg) + '_int'

    alternativa = {1: str(listaPreguntas2Basico[npregunta].alternativa1),
                   2: str(listaPreguntas2Basico[npregunta].alternativa2),
                   3: str(listaPreguntas2Basico[npregunta].alternativa3),
                   4: str(listaPreguntas2Basico[npregunta].alternativa4),
                   5: str(listaPreguntas2Basico[npregunta].alternativa5),
                   6: str(listaPreguntas2Basico[npregunta].alternativa6),
                   7: str(listaPreguntas2Basico[npregunta].alternativa7),
                   8: str(listaPreguntas2Basico[npregunta].alternativa8)
                   }

    data = {
        'img': imagen_ejercicio,
        'nombre_actividad': prueba,
        'descripcion_actividades': descripcion,
        'botones': posicion_boton,
        'npregunta': npreg,
        'tipo_ejercicio': tipo_ejercicio,
        'audio_pregunta': audio_pregunta,
        'total_ejercicios': total_ejercicios,
        'alternativa': alternativa
    }

    return render(request, 'ggalbas/visorActividades.html', data)

def guardaRespuesta(request):

    # parametros de sesion.
    rutAlumno = request.session['rut']
    pruebaGuia = request.session['prueba_guia']
    prueba = request.session['prueba']

    # parametros enviados por POST.
    respuestaAlumno = request.POST['respuestaAlumno']

    # parametro de fecha.
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")
    response = {}
    bd = 'e_test'

    # consultar el objeto alumno.
    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    # consulta la respuesta del alumno.
    listaTblAlumnoRespuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=objAlumno[0], prueba_guia=pruebaGuia)

    if listaTblAlumnoRespuestas:
        npregunta = int(listaTblAlumnoRespuestas.last().npregunta) + 1
    else:
        # es la primera pregunta.
        npregunta = 1

        # crea la actividad del alumno en tabla tbl_alumno_actividades.
        objContenidoFaseActividad = TblContenidosFasesActividades.objects.filter(id_contenido__id_contenido__isnull=True, id_fase__id_fase=1, id_actividad__nombre_actividad=prueba)

        if objContenidoFaseActividad:

            objAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad=objContenidoFaseActividad[0])
            if not objAlumnoActividades:
                registro = TblAlumnoActividades(rut_alumno=objAlumno[0], id_contenido_fase_actividad=objContenidoFaseActividad[0], fecha_inicio=fechaActual, intento=1)
                try:
                    registro.save()
                except:
                    print('falla al guardar')
            # end if.
        # end if.
    # end if.

    # consultar la pregunta de la prueba.
    listaPreguntas2Basico = Preguntas2Basico.objects.using('e_test').filter(idprueba=pruebaGuia, npregunta=npregunta)

    num_campos_completar = int(listaPreguntas2Basico[0].num_campos_completar)
    tipo_ejercicio = int(listaPreguntas2Basico[0].tipo_ejercicio)


    # Consulta la respuesta correcta de la pregunta.
    listaPreguntasInstancias = PreguntasInstancias.objects.using(bd).filter(idprueba=pruebaGuia, npregunta=npregunta)

    respuesta_pregunta = listaPreguntasInstancias[0].respuesta_pregunta
    instancia = 0

    if tipo_ejercicio == 1:  # ejercicios de tipo fill

        arrayRespuestaCorrecta = respuesta_pregunta.split(sep='~')
        arrayRespuestaAlumno = respuestaAlumno.split(sep='~')
        cantidadRespuestasCorrecta = 0

        for x in range(num_campos_completar):
            if arrayRespuestaCorrecta[x] == arrayRespuestaAlumno[x]:
                cantidadRespuestasCorrecta += 1
            # end if.
        # end for.

        instancia = int(cantidadRespuestasCorrecta) / num_campos_completar

    elif tipo_ejercicio == 2:

        if respuesta_pregunta == respuestaAlumno:
            instancia = 1
        else:
            instancia = 0
    # end if.

    elif tipo_ejercicio == 3:  # ejercicios de tipo

        listaRespuestas = respuesta_pregunta.replace('~', ",").split(sep=',')
        if listaRespuestas[0] == respuestaAlumno:
            instancia = 1
        else:
            instancia = 0

    # guarda la respuesta del alumno.
    registroRespuesta = TblAlumnoRespuestas(rut_alumno=objAlumno[0], npregunta=npregunta, prueba_guia=pruebaGuia, respuesta_alumno=respuestaAlumno, aprobada=instancia, fecha=fechaActual)

    try:
        registroRespuesta.save()
        response['alumnoRespuesta'] = True
    except:
        response['alumnoRespuesta'] = False

    # consultar el total de preguntas.
    totalPreg = Pruebas.objects.using('e_test').filter(idprueba=pruebaGuia)

    if int(totalPreg[0].npreguntas) == int(registroRespuesta.npregunta):
        response['fin'] = True
    else:
        response['fin'] = False

    responde = json.dumps(response)

    return HttpResponse(responde)

def calculoDiagnostico(rut_alumno, nombre_actividad, pais):

    respuesta = {'estatus': 1, 'mensaje': '', 'punto_prerequisito': '', 'punto_nivel': ''}

    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    fecha_fin = fechaActual
    fecha_inicio = fechaActual

    HabilidadPreg = dict()
    EjePreg = dict()

    tipoPregunta = dict()
    preguntaGuiado = dict()
    preguntaDiferenciado = dict()

    totalPregHabilidadGuiado = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    totalPregEjeGuiado = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

    totalPregHabilidadDiferenciado = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    totalPregEjeDiferenciado = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

    respCorrectaHabilidadGuiado = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    respCorrectaEjeGuiado = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

    respCorrectaHabilidadDiferenciado = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    respCorrectaEjeDiferenciado = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0}

    totalPregPrerequisitoGuiado = 0
    totalPregNivelGuiado = 0

    totalPregPrerequisitoDiferenciado = 0
    totalPregNivelDiferenciado = 0

    respuestasCorrectaPrerequisitoGuiado = 0
    respuestasCorrectaNivelGuiado = 0
    respuestasCorrectaPrerequisitoDiferenciado = 0
    respuestasCorrectaNivelDiferenciado = 0

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    if len(objAlumno) == 0:
        respuesta['estatus'] = 0
        respuesta['mensaje'] = 'El rut del alumno no existe, verifique.'
        return respuesta

    objActividad = TblActividades.objects.filter(nombre_actividad=nombre_actividad)

    if len(objActividad) == 0:
        respuesta['estatus'] = 0
        respuesta['mensaje'] = 'el nombre de la prueba no existe, verifique.'
        return respuesta

    # Determinar cual es la actividad Guiada y la diferenciada.
    if objActividad[0].id_padre is None:
        objActividadGuiado = objActividad[0]
        objTblActividades = TblActividades.objects.filter(id_padre=objActividad[0].id_actividad)
        objActividadDiferenciado = objTblActividades[0]

    else:
        objActividadDiferenciado = objActividad[0]
        objTblActividades = TblActividades.objects.filter(id_actividad=objActividad[0].id_padre)
        objActividadGuiado = objTblActividades[0]

    siglas_actividad = ''

    if pais == 'cl':
        siglas_actividad = nombre_actividad[0:2]  # obtengo las dos primeras siglas del nombre de la actividad.

    if pais == 'pe':
        siglas_actividad = nombre_actividad[0:3]  # obtengo las dos primeras siglas del nombre de la actividad.

    # consulta las preguntas del diagnostico para conocer ejes y habilidades.
    listaTblPreguntas = TblPreguntas.objects.filter(siglas=siglas_actividad)

    if len(listaTblPreguntas) == 0:
        respuesta['estatus'] = 0
        respuesta['mensaje'] = 'no se encontro el diagnostico en tbl_preguntas.'
        return respuesta

    for objTblPreguntas in listaTblPreguntas:

        if int(objTblPreguntas.id_tipo_pregunta.id_tipo_pregunta) == 1 and int(objTblPreguntas.guiado) == 1:
            totalPregPrerequisitoGuiado += 1

        if int(objTblPreguntas.id_tipo_pregunta.id_tipo_pregunta) == 2 and int(objTblPreguntas.guiado) == 1:
            totalPregNivelGuiado += 1

        if int(objTblPreguntas.id_tipo_pregunta.id_tipo_pregunta) == 1 and int(objTblPreguntas.diferenciado) == 1:
            totalPregPrerequisitoDiferenciado += 1

        if int(objTblPreguntas.id_tipo_pregunta.id_tipo_pregunta) == 2 and int(objTblPreguntas.diferenciado) == 1:
            totalPregNivelDiferenciado += 1

        tipoPregunta[objTblPreguntas.npregunta] = int(objTblPreguntas.id_tipo_pregunta.id_tipo_pregunta)

        preguntaGuiado[objTblPreguntas.npregunta] = True if int(objTblPreguntas.guiado) == 1 else False

        preguntaDiferenciado[objTblPreguntas.npregunta] = True if int(objTblPreguntas.diferenciado) == 1 else False

        HabilidadPreg[objTblPreguntas.npregunta] = int(objTblPreguntas.id_habilidad.id_habilidad)

        EjePreg[objTblPreguntas.npregunta] = int(objTblPreguntas.id_eje.id_eje)

        if int(objTblPreguntas.guiado) == 1:
            totalPregHabilidadGuiado[int(objTblPreguntas.id_habilidad.id_habilidad)] += 1
            totalPregEjeGuiado[int(objTblPreguntas.id_eje.id_eje)] += 1

        if int(objTblPreguntas.diferenciado) == 1:
            totalPregHabilidadDiferenciado[int(objTblPreguntas.id_habilidad.id_habilidad)] += 1
            totalPregEjeDiferenciado[int(objTblPreguntas.id_eje.id_eje)] += 1

    totalPreguntasDiagnostico = Preguntas2Basico.objects.using('e_test').filter(idprueba=objActividad[0].prueba_guia).count()

    cantPregAlumno = TblAlumnoRespuestas.objects.filter(rut_alumno=objAlumno[0], prueba_guia=objActividad[0].prueba_guia).count()

    # si el alumno no respondio preguntas se autocompleta por sistema.
    if cantPregAlumno < totalPreguntasDiagnostico:

        for npregunta in range(cantPregAlumno+1, totalPreguntasDiagnostico+1):

            objTblAlumnoRespuestas = TblAlumnoRespuestas(rut_alumno=objAlumno[0], npregunta=npregunta, prueba_guia=objActividad[0].prueba_guia, respuesta_alumno='AutoCompletado por Sistema', aprobada=0, fecha=fechaActual)

            try:
                objTblAlumnoRespuestas.save()
            except:
                print('error al guardar')

    listaTblAlumnoRespuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=objAlumno[0], prueba_guia=objActividad[0].prueba_guia).order_by('npregunta')

    if listaTblAlumnoRespuestas:

        primeraRespuesta = listaTblAlumnoRespuestas.first()
        fecha_inicio = primeraRespuesta.fecha
        UltimaRespuesta = listaTblAlumnoRespuestas.last()
        fecha_fin = UltimaRespuesta.fecha

        for objTblAlumnoRespuestas in listaTblAlumnoRespuestas:

            aprobada = 0 if objTblAlumnoRespuestas.aprobada < 1 else objTblAlumnoRespuestas.aprobada

            if int(tipoPregunta[objTblAlumnoRespuestas.npregunta]) == 1 and bool(preguntaGuiado[objTblAlumnoRespuestas.npregunta]):
                respuestasCorrectaPrerequisitoGuiado += aprobada

            if int(tipoPregunta[objTblAlumnoRespuestas.npregunta]) == 2 and bool(preguntaGuiado[objTblAlumnoRespuestas.npregunta]):
                respuestasCorrectaNivelGuiado += aprobada

            if int(tipoPregunta[objTblAlumnoRespuestas.npregunta]) == 1 and bool(preguntaDiferenciado[objTblAlumnoRespuestas.npregunta]):
                respuestasCorrectaPrerequisitoDiferenciado += aprobada

            if int(tipoPregunta[objTblAlumnoRespuestas.npregunta]) == 2 and bool(preguntaDiferenciado[objTblAlumnoRespuestas.npregunta]):
                respuestasCorrectaNivelDiferenciado += aprobada

            if bool(preguntaGuiado[objTblAlumnoRespuestas.npregunta]):
                respCorrectaHabilidadGuiado[int(HabilidadPreg[objTblAlumnoRespuestas.npregunta])] += aprobada
                respCorrectaEjeGuiado[int(EjePreg[objTblAlumnoRespuestas.npregunta])] += aprobada

            if bool(preguntaDiferenciado[objTblAlumnoRespuestas.npregunta]):
                respCorrectaHabilidadDiferenciado[int(HabilidadPreg[objTblAlumnoRespuestas.npregunta])] += aprobada
                respCorrectaEjeDiferenciado[int(EjePreg[objTblAlumnoRespuestas.npregunta])] += aprobada

    # Guiado.
    porcentajePrerequisitoGuiado = redondeo(respuestasCorrectaPrerequisitoGuiado * 100 / totalPregPrerequisitoGuiado) if totalPregPrerequisitoGuiado > 0 else 0
    porcentajePrerequisitoGuiado = 1 if porcentajePrerequisitoGuiado == 0 else porcentajePrerequisitoGuiado

    porcentajeNivelGuiado = redondeo(respuestasCorrectaNivelGuiado * 100 / totalPregNivelGuiado) if totalPregNivelGuiado > 0 else 0
    porcentajeNivelGuiado = 1 if porcentajeNivelGuiado == 0 else porcentajeNivelGuiado

    porcentajeH1Guiado = redondeo(respCorrectaHabilidadGuiado[1] * 100 / totalPregHabilidadGuiado[1]) if totalPregHabilidadGuiado[1] > 0 else 0
    porcentajeH2Guiado = redondeo(respCorrectaHabilidadGuiado[2] * 100 / totalPregHabilidadGuiado[2]) if totalPregHabilidadGuiado[2] > 0 else 0
    porcentajeH3Guiado = redondeo(respCorrectaHabilidadGuiado[3] * 100 / totalPregHabilidadGuiado[3]) if totalPregHabilidadGuiado[3] > 0 else 0

    porcentajeEje1Guiado = redondeo(respCorrectaEjeGuiado[1] * 100 / totalPregEjeGuiado[1]) if totalPregEjeGuiado[1] > 0 else 0
    porcentajeEje2Guiado = redondeo(respCorrectaEjeGuiado[2] * 100 / totalPregEjeGuiado[2]) if totalPregEjeGuiado[2] > 0 else 0
    porcentajeEje3Guiado = redondeo(respCorrectaEjeGuiado[3] * 100 / totalPregEjeGuiado[3]) if totalPregEjeGuiado[3] > 0 else 0
    porcentajeEje4Guiado = redondeo(respCorrectaEjeGuiado[4] * 100 / totalPregEjeGuiado[4]) if totalPregEjeGuiado[4] > 0 else 0
    porcentajeEje5Guiado = redondeo(respCorrectaEjeGuiado[5] * 100 / totalPregEjeGuiado[5]) if totalPregEjeGuiado[5] > 0 else 0
    porcentajeEje6Guiado = redondeo(respCorrectaEjeGuiado[6] * 100 / totalPregEjeGuiado[6]) if totalPregEjeGuiado[6] > 0 else 0
    porcentajeEje7Guiado = redondeo(respCorrectaEjeGuiado[7] * 100 / totalPregEjeGuiado[7]) if totalPregEjeGuiado[7] > 0 else 0
    porcentajeEje8Guiado = redondeo(respCorrectaEjeGuiado[8] * 100 / totalPregEjeGuiado[8]) if totalPregEjeGuiado[8] > 0 else 0
    porcentajeEje9Guiado = redondeo(respCorrectaEjeGuiado[9] * 100 / totalPregEjeGuiado[9]) if totalPregEjeGuiado[9] > 0 else 0
    porcentajeEje10Guiado = redondeo(respCorrectaEjeGuiado[10] * 100 / totalPregEjeGuiado[10]) if totalPregEjeGuiado[10] > 0 else 0

    # Diferenciado.
    porcentajePrerequisitoDiferenciado = redondeo(respuestasCorrectaPrerequisitoDiferenciado * 100 / totalPregPrerequisitoDiferenciado) if totalPregPrerequisitoDiferenciado > 0 else 0
    porcentajePrerequisitoDiferenciado = 1 if porcentajePrerequisitoDiferenciado == 0 else porcentajePrerequisitoDiferenciado

    porcentajeNivelDiferenciado = redondeo(respuestasCorrectaNivelDiferenciado * 100 / totalPregNivelDiferenciado) if totalPregNivelDiferenciado > 0 else 0
    porcentajeNivelDiferenciado = 1 if porcentajeNivelDiferenciado == 0 else porcentajeNivelDiferenciado

    porcentajeH1Diferenciado = redondeo(respCorrectaHabilidadDiferenciado[1] * 100 / totalPregHabilidadDiferenciado[1]) if totalPregHabilidadDiferenciado[1] > 0 else 0
    porcentajeH2Diferenciado = redondeo(respCorrectaHabilidadDiferenciado[2] * 100 / totalPregHabilidadDiferenciado[2]) if totalPregHabilidadDiferenciado[2] > 0 else 0
    porcentajeH3Diferenciado = redondeo(respCorrectaHabilidadDiferenciado[3] * 100 / totalPregHabilidadDiferenciado[3]) if totalPregHabilidadDiferenciado[3] > 0 else 0

    porcentajeEje1Diferenciado = redondeo(respCorrectaEjeDiferenciado[1] * 100 / totalPregEjeDiferenciado[1]) if totalPregEjeDiferenciado[1] > 0 else 0
    porcentajeEje2Diferenciado = redondeo(respCorrectaEjeDiferenciado[2] * 100 / totalPregEjeDiferenciado[2]) if totalPregEjeDiferenciado[2] > 0 else 0
    porcentajeEje3Diferenciado = redondeo(respCorrectaEjeDiferenciado[3] * 100 / totalPregEjeDiferenciado[3]) if totalPregEjeDiferenciado[3] > 0 else 0
    porcentajeEje4Diferenciado = redondeo(respCorrectaEjeDiferenciado[4] * 100 / totalPregEjeDiferenciado[4]) if totalPregEjeDiferenciado[4] > 0 else 0
    porcentajeEje5Diferenciado = redondeo(respCorrectaEjeDiferenciado[5] * 100 / totalPregEjeDiferenciado[5]) if totalPregEjeDiferenciado[5] > 0 else 0
    porcentajeEje6Diferenciado = redondeo(respCorrectaEjeDiferenciado[6] * 100 / totalPregEjeDiferenciado[6]) if totalPregEjeDiferenciado[6] > 0 else 0
    porcentajeEje7Diferenciado = redondeo(respCorrectaEjeDiferenciado[7] * 100 / totalPregEjeDiferenciado[7]) if totalPregEjeDiferenciado[7] > 0 else 0
    porcentajeEje8Diferenciado = redondeo(respCorrectaEjeDiferenciado[8] * 100 / totalPregEjeDiferenciado[8]) if totalPregEjeDiferenciado[8] > 0 else 0
    porcentajeEje9Diferenciado = redondeo(respCorrectaEjeDiferenciado[9] * 100 / totalPregEjeDiferenciado[9]) if totalPregEjeDiferenciado[9] > 0 else 0
    porcentajeEje10Diferenciado = redondeo(respCorrectaEjeDiferenciado[10] * 100 / totalPregEjeDiferenciado[10]) if totalPregEjeDiferenciado[10] > 0 else 0


    # verificar si existe el registro en tbl_alumno_diagnostico.
    objTblAlumnoDiagnostico = TblAlumnoDiagnostico.objects.filter(rut_alumno=objAlumno[0], id_actividad=objActividadGuiado)

    if objTblAlumnoDiagnostico:
        # actualizar.
        objTblAlumnoDiagnostico.update(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                                       punto_prerequisito=porcentajePrerequisitoGuiado,
                                       punto_nivel=porcentajeNivelGuiado, h1=porcentajeH1Guiado, h2=porcentajeH2Guiado,
                                       h3=porcentajeH3Guiado, eje1=porcentajeEje1Guiado, eje2=porcentajeEje2Guiado,
                                       eje3=porcentajeEje3Guiado, eje4=porcentajeEje4Guiado, eje5=porcentajeEje5Guiado,
                                       eje6=porcentajeEje6Guiado, eje7=porcentajeEje7Guiado, eje8=porcentajeEje8Guiado,
                                       eje9=porcentajeEje9Guiado, eje10=porcentajeEje10Guiado)

    else:
        # insertar.
        registroGuiado = TblAlumnoDiagnostico(rut_alumno=objAlumno[0], id_actividad=objActividadGuiado,
                                              fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                                              punto_prerequisito=porcentajePrerequisitoGuiado,
                                              punto_nivel=porcentajeNivelGuiado, h1=porcentajeH1Guiado,
                                              h2=porcentajeH2Guiado, h3=porcentajeH3Guiado, eje1=porcentajeEje1Guiado,
                                              eje2=porcentajeEje2Guiado, eje3=porcentajeEje3Guiado,
                                              eje4=porcentajeEje4Guiado, eje5=porcentajeEje5Guiado,
                                              eje6=porcentajeEje6Guiado, eje7=porcentajeEje7Guiado,
                                              eje8=porcentajeEje8Guiado, eje9=porcentajeEje9Guiado,
                                              eje10=porcentajeEje10Guiado)
        try:
            registroGuiado.save()
        except:
            respuesta['estatus'] = 0
            respuesta['mensaje'] = 'error al guardar en tbl_alumno_diagnostico.'
            return respuesta


    # verificar si existe el registro en tbl_alumno_diagnostico.
    objTblAlumnoDiagnostico = TblAlumnoDiagnostico.objects.filter(rut_alumno=objAlumno[0], id_actividad=objActividadDiferenciado)

    if objTblAlumnoDiagnostico:
        # actualizar.
        objTblAlumnoDiagnostico.update(fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                                       punto_prerequisito=porcentajePrerequisitoDiferenciado,
                                       punto_nivel=porcentajeNivelDiferenciado, h1=porcentajeH1Diferenciado,
                                       h2=porcentajeH2Diferenciado, h3=porcentajeH3Diferenciado,
                                       eje1=porcentajeEje1Diferenciado, eje2=porcentajeEje2Diferenciado,
                                       eje3=porcentajeEje3Diferenciado, eje4=porcentajeEje4Diferenciado,
                                       eje5=porcentajeEje5Diferenciado, eje6=porcentajeEje6Diferenciado,
                                       eje7=porcentajeEje7Diferenciado, eje8=porcentajeEje8Diferenciado,
                                       eje9=porcentajeEje9Diferenciado, eje10=porcentajeEje10Diferenciado)

    else:
        # insertar.
        registroDiferenciado = TblAlumnoDiagnostico(rut_alumno=objAlumno[0], id_actividad=objActividadDiferenciado,
                                                    fecha_inicio=fecha_inicio, fecha_fin=fecha_fin,
                                                    punto_prerequisito=porcentajePrerequisitoDiferenciado,
                                                    punto_nivel=porcentajeNivelDiferenciado,
                                                    h1=porcentajeH1Diferenciado, h2=porcentajeH2Diferenciado,
                                                    h3=porcentajeH3Diferenciado, eje1=porcentajeEje1Diferenciado,
                                                    eje2=porcentajeEje2Diferenciado, eje3=porcentajeEje3Diferenciado,
                                                    eje4=porcentajeEje4Diferenciado, eje5=porcentajeEje5Diferenciado,
                                                    eje6=porcentajeEje6Diferenciado, eje7=porcentajeEje7Diferenciado,
                                                    eje8=porcentajeEje8Diferenciado, eje9=porcentajeEje9Diferenciado,
                                                    eje10=porcentajeEje10Diferenciado)
        try:
            registroDiferenciado.save()
        except:
            respuesta['estatus'] = 0
            respuesta['mensaje'] = 'error al guardar en tbl_alumno_diagnostico.'
            return respuesta

    # actualizar en tbl_alumno.
    try:
        objAlumno.update(nuevo=0)
    except:
        respuesta['estatus'] = 0
        respuesta['mensaje'] = 'error al actualizar en tbl_alumno.'
        return respuesta

    puntajeActividad = ''

    if int(objAlumno[0].id_producto.id_producto) == 2:  # es alumno emat Guiado

        puntajeActividad = porcentajePrerequisitoGuiado
        respuesta['punto_prerequisito'] = porcentajePrerequisitoGuiado
        respuesta['punto_nivel'] = porcentajeNivelGuiado

    if int(objAlumno[0].id_producto.id_producto) == 3:  # es alumno emat Diferenciado

        puntajeActividad = porcentajePrerequisitoDiferenciado
        respuesta['punto_prerequisito'] = porcentajePrerequisitoDiferenciado
        respuesta['punto_nivel'] = porcentajeNivelDiferenciado

    # actualizar en tbl_alumno_actividades.
    TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_actividad__prueba_guia=int(objActividad[0].prueba_guia)).update(fecha_fin=fecha_fin, puntaje=puntajeActividad)

    return respuesta

def calculoDiagnosticoAdmin(request):

    respuesta = {'estatus': 1, 'mensaje': '', 'punto_prerequisito': '', 'punto_nivel': ''}

    if "rut" in request.POST:
        rut = request.POST["rut"]
    else:
        respuesta['estatus'] = 0
        respuesta['mensaje'] = 'El numero de rut no puede estar vacio, verifique.'
        return respuesta

    if "prueba" in request.POST:
        prueba = request.POST["prueba"]
    else:
        respuesta['estatus'] = 0
        respuesta['mensaje'] = 'El nombre de actividad no puede estar vacio, verifique.'
        return respuesta

    pais = flagPais(request)

    return calculoDiagnostico(rut, prueba, pais)

def cierreEvaluacionesAnuales(request):

    now = datetime.datetime.now()
    pais = flagPais(request)

    res = '<b>Listado de Alumnos con Diagnostico Sin Finalizar.</b>'

    listaTblAlumnoActividades = TblAlumnoActividades.objects.filter(fecha_fin__isnull=True, puntaje__isnull=True, id_contenido_fase_actividad__id_fase__id_fase=1).order_by('id_contenido_fase_actividad__id_actividad__nombre_actividad')

    if listaTblAlumnoActividades:
        contador = 0
        for objTblAlumnoActividades in listaTblAlumnoActividades:
            contador = contador + 1
            res = res + "<br>" + str(contador) + "- <b>Rut:</b> " + str(objTblAlumnoActividades.rut_alumno.rut_alumno) + ", <b>codigo lista:</b> " + str(objTblAlumnoActividades.rut_alumno.codigo_lista.codigo_lista) + ", <b>Nombre de la actividad:</b> " + str(objTblAlumnoActividades.id_contenido_fase_actividad.id_actividad.nombre_actividad) + ", <b>fecha de inicio:</b> " + str(objTblAlumnoActividades.fecha_inicio) + ", <b>Dias transcurridos:</b> " + str((now - objTblAlumnoActividades.fecha_inicio).days)

            if int((now - objTblAlumnoActividades.fecha_inicio).days) >= 14 and objTblAlumnoActividades.rut_alumno.codigo_lista.cierre_diagnostico == 0:
                # cierra el diagnostico.
                result = calculoDiagnostico(str(objTblAlumnoActividades.rut_alumno.rut_alumno), str(objTblAlumnoActividades.id_contenido_fase_actividad.id_actividad.nombre_actividad), pais)
                res = res + ", <b>Estatus:</b> " + str(result['estatus']) + ",<b>Mensaje:</b> " + str(result['mensaje']) + ", <b>punto_prerequisito:</b> " + str(result['punto_prerequisito']) + ", <b>punto_nivel:</b>" + str(result['punto_nivel'])
            else:
                res = res + ", <b>Estatus:</b> Sin Procesar."
    else:
        res = res + '<br>No hay alumnos con Diagnostico iniciado.'

    res = res + '<br>FIN DE PROCESO.'

    return HttpResponse(res)

def portadaFinalDiagnostico(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    pais = flagPais(request)

    pruebaGuia = request.session['prueba_guia']

    objActividad = TblActividades.objects.filter(prueba_guia=pruebaGuia)
    descripcion = objActividad[0].descripcion_actividades

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    if objAlumno[0].id_producto.id_producto == 2:
        idActividad = objActividad[0]
    else:
        actividadDiferenciada = TblActividades.objects.filter(id_padre=int(objActividad[0].id_actividad))
        idActividad = actividadDiferenciada[0]

    objAlumnoDiagnostico = TblAlumnoDiagnostico.objects.filter(rut_alumno=objAlumno[0], id_actividad=idActividad)

    if objAlumnoDiagnostico:

        punto_prerequisito = int(objAlumnoDiagnostico[0].punto_prerequisito)
        punto_nivel = int(objAlumnoDiagnostico[0].punto_nivel)
    else:

        respuesta = calculoDiagnostico(request.session['rut'], request.session['prueba'], pais)
        punto_prerequisito = respuesta['punto_prerequisito']
        punto_nivel = respuesta['punto_nivel']

    data = {
        'descripcion': descripcion,
        'punto_prerequisito': punto_prerequisito,
        'punto_nivel': punto_nivel,
    }

    return render(request, 'ggalbas/portadaFinalDiagnostico.html', data)

def unidadesAlumno(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    ordenUnidadTutor = 1  # por defecto, la primera unidad deberia estar habilitada.

    opcionActivacionUnidades = int(objAlumno[0].codigo_lista.activar_unidades)

    ordenUnidad = {}
    ordenContenido = {}
    dictContenidosUnidad = {}

    if objAlumno[0].autonomo == 0:

        listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad__orden', 'orden')

        for ObjContenidoUnidad in listaObjContenidoUnidad:

            ordenUnidad[int(ObjContenidoUnidad.id_contenido.id_contenido)] = int(ObjContenidoUnidad.id_unidad.orden)
            ordenContenido[int(ObjContenidoUnidad.id_contenido.id_contenido)] = int(ObjContenidoUnidad.orden)

            if ObjContenidoUnidad.activo == 1:
                ordenUnidadTutor = ObjContenidoUnidad.id_unidad.orden

            if ObjContenidoUnidad.id_unidad.orden not in dictContenidosUnidad:
                dictContenidosUnidad[ObjContenidoUnidad.id_unidad.orden] = []

            dictContenidosUnidad[ObjContenidoUnidad.id_unidad.orden].append(ObjContenidoUnidad)


    if objAlumno[0].autonomo == 1:

        listaTblPlanAutonomo = TblPlanAutonomo.objects.filter(rut_alumno=objAlumno[0]).order_by('id_unidad__orden', 'orden')

        for ObjTblPlanAutonomo in listaTblPlanAutonomo:

            ordenUnidad[int(ObjTblPlanAutonomo.id_contenido.id_contenido)] = int(ObjTblPlanAutonomo.id_unidad.orden)

            ordenContenido[int(ObjTblPlanAutonomo.id_contenido.id_contenido)] = int(ObjTblPlanAutonomo.orden)

            if ObjTblPlanAutonomo.id_unidad.orden not in dictContenidosUnidad:
                dictContenidosUnidad[ObjTblPlanAutonomo.id_unidad.orden] = []

            dictContenidosUnidad[ObjTblPlanAutonomo.id_unidad.orden].append(ObjTblPlanAutonomo)


    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase__in=[2, 3, 4]).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        try:
            contenidoPadre = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_padre
        except ObjectDoesNotExist:
            contenidoPadre = False
        if contenidoPadre:
            idContenidoActual=objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_padre
        else:
            idContenidoActual=objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido
        ordenUnidadActual = ordenUnidad[idContenidoActual]
        ordenContenidoActual = ordenContenido[idContenidoActual]


        if objUltimaActividadAlumno.puntaje is not None and objUltimaActividadAlumno.fecha_fin is not None:

            if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_tipo_actividad.id_tipo_actividad) == 1 and int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 4:

                if int(objUltimaActividadAlumno.intento) == 1 and int(objUltimaActividadAlumno.puntaje) >= 65:
                    ordenContenidoActual += 1

                if int(objUltimaActividadAlumno.intento) == 2 and int(objUltimaActividadAlumno.puntaje) >= 50:
                    ordenContenidoActual += 1

                if int(objUltimaActividadAlumno.intento) == 3:
                    ordenContenidoActual += 1


    else:
        # el alumno no ha iniciado ninguna actividad , esta en la unidad 1 y contenido con orden 1.
        ordenContenidoActual = 1
        ordenUnidadActual = 1


    data = {
        'dictContenidosUnidad': dictContenidosUnidad,
        'ordenUnidadActual': ordenUnidadActual,
        'ordenContenidoActual': ordenContenidoActual,
        'opcionActivacionUnidades': opcionActivacionUnidades,
        'ordenUnidadTutor': ordenUnidadTutor,
        'autonomo': objAlumno[0].autonomo,
    }

    return render(request, 'ggalbas/unidadesAlumno.html', data)

def contenidosAlumno(request):

    if request.session.get("rut", False):
        rutAlumno = request.session['rut']
    else:
        return redirect('index')

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    if objAlumno[0].id_producto.id_producto == 2:
        diferenciado = False
    else:
        diferenciado = True

    listaTodosContenidos = []
    ordenUnidad = {}

    if objAlumno[0].autonomo == 0:

        listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad__orden', 'orden')

        if diferenciado:
            for ObjContenidoUnidad in listaObjContenidoUnidad:
                contenidoDiferenciado=TblContenidos.objects.filter(id_padre=int(ObjContenidoUnidad.id_contenido.id_contenido))
                listaTodosContenidos.append(contenidoDiferenciado[0])
                ordenUnidad[int(contenidoDiferenciado[0].id_contenido)] = int(ObjContenidoUnidad.id_unidad.orden)
        else:
            for ObjContenidoUnidad in listaObjContenidoUnidad:
                listaTodosContenidos.append(ObjContenidoUnidad.id_contenido)
                ordenUnidad[int(ObjContenidoUnidad.id_contenido.id_contenido)] = int(ObjContenidoUnidad.id_unidad.orden)

    if objAlumno[0].autonomo == 1:

        listaObjContenidoUnidad = TblPlanAutonomo.objects.filter(rut_alumno=objAlumno[0]).order_by('id_unidad__orden', 'orden')

        for ObjTblPlanAutonomo in listaObjContenidoUnidad:
            listaTodosContenidos.append(ObjTblPlanAutonomo.id_contenido)
            ordenUnidad[int(ObjTblPlanAutonomo.id_contenido.id_contenido)] = int(ObjTblPlanAutonomo.id_unidad.orden)


    # diccionarios que guarda la suma de los puntajes por pregunta del minitest de 5 en 5 para cada actividad de la fase de recuperacion.
    puntajeActividadRecup = {2: 0, 3: 0, 4: 0}

    # consultar las ultimas actividades del alumno finalizadas.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase__in=[2, 3, 4], fecha_fin__isnull=False, puntaje__isnull=False).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        # consultar las actividades del contenido.
        if int(objUltimaActividadAlumno.diferenciado) == 1:
            if int(objAlumno[0].id_producto.id_producto) == 3:
                objContenidoActual = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido
            else:
                objContenidoPadre = TblContenidos.objects.filter(id_contenido=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_padre))
                objContenidoActual = objContenidoPadre[0]
        else:
            if int(objAlumno[0].id_producto.id_producto) == 2:
                objContenidoActual = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido
            else:
                objContenidoDiferenciado = TblContenidos.objects.filter(id_padre=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido))
                objContenidoActual = objContenidoDiferenciado[0]


        # obtengo la posicion de la ultima actividad finalizada.

        ordenUnidadActual = ordenUnidad[int(objContenidoActual.id_contenido)]
        ordenActividadActual = int(objUltimaActividadAlumno.id_contenido_fase_actividad.orden)

        # si la ultima actividad realizada es de la fase de minitest o de la fase de recuperacion.
        if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 2 or int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 3:
            # busco la actividad de minitest dentro de la lista de actividades.

            for ObjAlumnoActividades in listaObjAlumnoActividades:
                if int(ObjAlumnoActividades.diferenciado)==1:
                    if diferenciado:
                        contenido=objContenidoActual.id_contenido
                    else:
                        contenidoPadre=TblContenidos.objects.filter(id_padre=int(objContenidoActual.id_contenido))
                        contenido= contenidoPadre[0].id_contenido
                else:
                    if diferenciado:
                        contenido=objContenidoActual.id_padre
                    else:
                        contenido = objContenidoActual.id_contenido



                if int(ObjAlumnoActividades.id_contenido_fase_actividad.id_fase.id_fase) == 2 and int(ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_contenido) == contenido:
                    objActividadMinitest = ObjAlumnoActividades.id_contenido_fase_actividad.id_actividad
                    pruebaGuia = objActividadMinitest.prueba_guia
                # end if.

            # end for


            # buscar las respuestas del Minitest del contenido actual.
            listaTblAlumnoRespuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=objAlumno[0], prueba_guia=int(pruebaGuia)).order_by('npregunta')

            if listaTblAlumnoRespuestas:
                for objTblAlumnoRespuestas in listaTblAlumnoRespuestas:
                    if 1 <= int(objTblAlumnoRespuestas.npregunta) <= 5:
                        puntajeActividadRecup[2] += int(objTblAlumnoRespuestas.aprobada)
                    # end if.
                    if 6 <= int(objTblAlumnoRespuestas.npregunta) <= 10:
                        puntajeActividadRecup[3] += int(objTblAlumnoRespuestas.aprobada)
                    # end if.
                    if 11 <= int(objTblAlumnoRespuestas.npregunta) <= 15:
                        puntajeActividadRecup[4] += int(objTblAlumnoRespuestas.aprobada)
                    # end if.
                # end for.
            # end if

            ordenActividadActual += 1
            puntajeMinimoAprobacion = 3
            while ordenActividadActual <= 4:
                if puntajeActividadRecup[ordenActividadActual] >= puntajeMinimoAprobacion:
                    ordenActividadActual += 1
                else:
                    break
                # end if
            # end while

        # si la ultima actividad realizada es de la fase de Nivel.
        elif int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 4:
            actividad= objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad

            # si es una actividad de tipo Repaso (A5) de la fase de nivel entonces retrocedo.
            if int(actividad.id_tipo_actividad.id_tipo_actividad) == 4:
                ordenActividadActual = ordenActividadActual - 1

            # si es una actividad de evaluacion (A3) de la fase de nivel entonces verifico otras condiciones.
            elif int(actividad.id_tipo_actividad.id_tipo_actividad) == 1:
                # si aprobo con >= 65% en el intento 1 o si aprobo con >=50% en el intento 2 o si realizo un tercer intento.
                if (int(objUltimaActividadAlumno.puntaje) >= 65 and int(objUltimaActividadAlumno.intento) == 1) or (int(objUltimaActividadAlumno.puntaje) >= 50 and int(objUltimaActividadAlumno.intento) == 2) or int(objUltimaActividadAlumno.intento) == 3:
                    indexObjContenidoActual = listaTodosContenidos.index(objContenidoActual) # retorna el indice del contenido actual.

                    objContenidoActual = listaTodosContenidos[int(indexObjContenidoActual) + 1]  # obtengo el siguiente contenido.
                    ordenUnidadActual = ordenUnidad[int(objContenidoActual.id_contenido)]
                    ordenActividadActual = 1

                else:
                    if (int(objUltimaActividadAlumno.diferenciado) == 1 and int(objAlumno[0].id_producto.id_producto) == 3) or (int(objUltimaActividadAlumno.diferenciado) == 0 and int(objAlumno[0].id_producto.id_producto) == 2):
                        # el alumno reprobo, avanzo a la siguiente actividad de repaso.
                        ordenActividadActual += 1
                    else:
                        # si cambio de subproducto queda en el A3
                        ordenActividadActual = ordenActividadActual
                # end if.

            # es cualquier otra actividad de la fase de nivel, simplemente avanza a la siguiente actividad.
            else:
                ordenActividadActual += 1
            # end if

    # el alumno no ha iniciado ninguna actividad, esta en el Minitest del primer contenido.
    else:
        primerObjContenidoUnidad = listaObjContenidoUnidad.first()
        objContenidoActual = primerObjContenidoUnidad.id_contenido
        ordenUnidadActual = 1
        ordenActividadActual = 1
    # end if.

    # buscar todas las actividades del contenido donde se encuentra el alumno, agrupados por fases (minitest, recuperacion y nivel).
    listaObjContenidosFasesActividades = TblContenidosFasesActividades.objects.filter(id_contenido=objContenidoActual, id_fase__in=[2, 3, 4]).order_by('orden')

    ActividadesPorFase = {}

    if listaObjContenidosFasesActividades:

        for objContenidoFaseActividad in listaObjContenidosFasesActividades:
            if objContenidoFaseActividad.id_fase.id_fase not in ActividadesPorFase:
                ActividadesPorFase[int(objContenidoFaseActividad.id_fase.id_fase)] = []
            ActividadesPorFase[int(objContenidoFaseActividad.id_fase.id_fase)].append(objContenidoFaseActividad)

    data = {
        'ordenUnidadActual': ordenUnidadActual,
        'ordenActividadActual': ordenActividadActual,
        'nombre_contenido': str(objContenidoActual.descripcion),
        'ActividadesPorFase': ActividadesPorFase,
        'puntajeActividadRecup': puntajeActividadRecup
    }

    return render(request, 'ggalbas/contenidosAlumno.html', data)

def iniciarActividad(request):

    response = {'estatus': 1, 'mensaje': ''}

    now = datetime.datetime.now()
    fecha_actual = now.strftime("%Y-%m-%d %H:%M:%S")

    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    if objAlumno[0].id_producto.id_producto == 2:
        diferenciado = False
    else:
        diferenciado = True

    listaTodosContenidos = []
    dictContenidoUnidad = {}

    if objAlumno[0].autonomo == 0:
        listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad__orden', 'orden')

        if diferenciado:
            for ObjContenidoUnidad in listaObjContenidoUnidad:
                contenidoDiferenciado=TblContenidos.objects.filter(id_padre=int(ObjContenidoUnidad.id_contenido.id_contenido))
                listaTodosContenidos.append(contenidoDiferenciado[0])
                dictContenidoUnidad[int(contenidoDiferenciado[0].id_contenido)] = ObjContenidoUnidad
        else:
            for ObjContenidoUnidad in listaObjContenidoUnidad:
                listaTodosContenidos.append(ObjContenidoUnidad.id_contenido)
                dictContenidoUnidad[int(ObjContenidoUnidad.id_contenido.id_contenido)] = ObjContenidoUnidad

    if objAlumno[0].autonomo == 1:
        listaObjContenidoUnidad = TblPlanAutonomo.objects.filter(rut_alumno=objAlumno[0]).order_by('id_unidad__orden', 'orden')

        for ObjPlanAutonomo in listaObjContenidoUnidad:
            listaTodosContenidos.append(ObjPlanAutonomo.id_contenido)

    # consultar la ultima actividad iniciada por el alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase__in=[2, 3, 4]).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        ordenActividadActual = objUltimaActividadAlumno.id_contenido_fase_actividad.orden
        intento = 1
        # consultar las actividades del contenido.
        if int(objUltimaActividadAlumno.diferenciado) == 1:
            if int(objAlumno[0].id_producto.id_producto) == 3:
                objContenidoActual = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido
            else:
                objContenidoPadre = TblContenidos.objects.filter(id_contenido=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_padre))
                objContenidoActual = objContenidoPadre[0]
        else:
            if int(objAlumno[0].id_producto.id_producto) == 2:
                objContenidoActual = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido
            else:
                objContenidoDiferenciado = TblContenidos.objects.filter(
                    id_padre=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido))
                objContenidoActual = objContenidoDiferenciado[0]

        # si la ultima actividad no esta finalizada
        if objUltimaActividadAlumno.puntaje is None and objUltimaActividadAlumno.fecha_fin is None:
            # obtener el id de la actividad actual.
            response['id_fase'] = int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase)
            response['ultimaSiglasActividad'] = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad[-2:]
            response['siglasActividad'] = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad

        else:
            # si la ultima actividad realizada es de la fase de minitest o de la fase de recuperacion.
            if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 2 or int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 3:

                intento = 1
                # busco la actividad de minitest dentro de la lista de actividades.

                for ObjAlumnoActividades in listaObjAlumnoActividades:
                    if int(ObjAlumnoActividades.id_contenido_fase_actividad.id_fase.id_fase) == 2:
                        objActividadMinitest = ObjAlumnoActividades.id_contenido_fase_actividad.id_actividad

                    # end if.
                # end for

                # buscar las respuestas del Minitest del contenido.
                listaTblAlumnoRespuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=objAlumno[0], prueba_guia=int(objActividadMinitest.prueba_guia)).order_by('npregunta')

                # diccionarios que guarda la suma de los puntajes por pregunta del minitest de 5 en 5 para cada actividad de la fase de recuperacion.
                puntajeActividadRecup = {2: 0, 3: 0, 4: 0}

                if listaTblAlumnoRespuestas:

                    for objTblAlumnoRespuestas in listaTblAlumnoRespuestas:

                        if 1 <= int(objTblAlumnoRespuestas.npregunta) <= 5:
                            puntajeActividadRecup[2] += int(objTblAlumnoRespuestas.aprobada)
                        # end if.

                        if 6 <= int(objTblAlumnoRespuestas.npregunta) <= 10:
                            puntajeActividadRecup[3] += int(objTblAlumnoRespuestas.aprobada)
                        # end if.

                        if 11 <= int(objTblAlumnoRespuestas.npregunta) <= 15:
                            puntajeActividadRecup[4] += int(objTblAlumnoRespuestas.aprobada)
                        # end if.
                # end if

                ordenActividadActual += 1
                puntajeMinimoAprobacion = 3

                while ordenActividadActual <= 4:
                    if puntajeActividadRecup[ordenActividadActual] >= puntajeMinimoAprobacion:
                        ordenActividadActual += 1
                    else:
                        break
                    # end if
                # end while

            # si la ultima actividad es de la fase de nivel.
            elif int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 4:

                # Si la ultima actividad realizada es de tipo Evaluacion (A3) de la fase de nivel, entonces verifico otras condiciones.,
                if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_tipo_actividad.id_tipo_actividad) == 1:
                    actividadAlumno = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0],id_contenido_fase_actividad=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido_fase_actividad)).order_by('fecha_inicio')
                    if (int(actividadAlumno.last().puntaje) >= 65 and int(actividadAlumno.last().intento) == 1) or (int(actividadAlumno.last().puntaje) >= 50 and int(actividadAlumno.last().intento) == 2) or int(actividadAlumno.last().intento) == 3:

                        if int(objUltimaActividadAlumno.diferenciado) == 1:
                            if diferenciado:
                                contenidoActual = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido
                            else:
                                objContenido = TblContenidos.objects.filter(id_contenido=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_padre))
                                contenidoActual = objContenido[0]
                        else:
                            if diferenciado:
                                objContenido = TblContenidos.objects.filter(id_padre=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido))
                                contenidoActual = objContenido[0]
                            else:
                                contenidoActual = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido

                        ordenActividadActual = 1
                        intento = 1
                        indexObjContenidoActual = listaTodosContenidos.index(contenidoActual)  # metodo index retorna el indice del contenido actual.
                        objContenidoActual = listaTodosContenidos[int(indexObjContenidoActual) + 1]  # siguiente contenido.

                        # consulta ultimo registro en tabla tbl_plan del alumno.
                        regPlan = TblPlan(rut_alumno=objAlumno[0],
                                          id_contenido_unidad=dictContenidoUnidad[int(objContenidoActual.id_contenido)],
                                          fecha_inicio=fecha_actual)
                        try:
                            regPlan.save()
                        except:
                            response = {'estatus': 0, 'mensaje': 'error al guardar en la tabla tbl_plan.'}

                    else:

                        if (diferenciado and int(objUltimaActividadAlumno.diferenciado == 1)) or (not diferenciado and int(objUltimaActividadAlumno.diferenciado == 0)):
                            ordenActividadActual = int(ordenActividadActual) + 1
                            intento = int(actividadAlumno.last().intento)

                        else:

                            if diferenciado:
                                tipo = 1
                            else:
                                tipo = 0

                            ordenActividadActual = int(ordenActividadActual)

                            cantidadEvaluaciones = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_contenido=objContenidoActual, id_contenido_fase_actividad__id_fase__id_fase=4, id_contenido_fase_actividad__id_actividad__id_tipo_actividad__id_tipo_actividad=1, diferenciado=tipo).count()
                            intento = int(cantidadEvaluaciones) + 1


                # Si la ultima actividad realizada es de tipo Repaso (A5) de la fase de nivel, entonces regreso a la actividad de evaluacion (A3)
                elif int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_tipo_actividad.id_tipo_actividad) == 4:
                    ordenActividadActual = int(ordenActividadActual) - 1


                    if diferenciado:
                        tipo=1
                    else:
                        tipo=0
                    actividadActual=TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0],id_contenido_fase_actividad__id_fase__id_fase__in=[4], id_contenido_fase_actividad__id_actividad__id_tipo_actividad__id_tipo_actividad__in=[1], diferenciado=tipo).order_by('fecha_inicio')
                    if actividadActual:
                        if int(actividadActual.last().id_contenido_fase_actividad.id_contenido.id_contenido)==int(objContenidoActual.id_contenido):
                            objEvaluacionAnterior = actividadActual.last()
                            intento = int(objEvaluacionAnterior.intento) + 1
                        else:
                            intento = 1
                else:
                    # para las otras actividades de la fase de nivel simplemente avanza a la siguiente actividad.
                    ordenActividadActual = int(ordenActividadActual) + 1
                    intento = 1



            listaObjContenidosFasesActividades = TblContenidosFasesActividades.objects.filter(id_contenido=objContenidoActual, id_fase__in=[2, 3, 4]).order_by('orden')

            dictActividades = {}

            if listaObjContenidosFasesActividades:

                for ObjContenidosFasesActividades in listaObjContenidosFasesActividades:
                    dictActividades[int(ObjContenidosFasesActividades.orden)] = ObjContenidosFasesActividades

                response['id_fase'] = int(dictActividades[ordenActividadActual].id_fase.id_fase)
                response['siglasActividad'] = dictActividades[ordenActividadActual].id_actividad.nombre_actividad
                response['ultimaSiglasActividad'] = dictActividades[ordenActividadActual].id_actividad.nombre_actividad[-2:]

                if diferenciado:
                    id_diferenciado = 1
                else:
                    id_diferenciado = 0

                # guardar en la tabla tbl_alumno_actividad
                regAlumnoActividades = TblAlumnoActividades(rut_alumno=objAlumno[0], id_contenido_fase_actividad=dictActividades[ordenActividadActual], fecha_inicio=fecha_actual, intento=intento, diferenciado=id_diferenciado)
                try:
                    regAlumnoActividades.save()
                except:
                    response = {'estatus': 0, 'mensaje': 'error al guardar en tabla tbl_alumno_actividades, intente de nuevo.'}

    else:

        # el alumno no ha iniciado ninguna actividad, esta en la primera actividad del primer contenido.
        primerObjContenidoUnidad = listaObjContenidoUnidad.first()
        if diferenciado:
            objContenidoDiferenciado=TblContenidos.objects.filter(id_padre=int(primerObjContenidoUnidad.id_contenido.id_contenido))
            objContenidoActual=objContenidoDiferenciado[0]
        else:
            objContenidoActual = primerObjContenidoUnidad.id_contenido
        ordenActividadActual = 1
        intento = 1

        # consultar las actividades del contenido donde se encuentra el alumno.
        listaObjContenidosFasesActividades = TblContenidosFasesActividades.objects.filter(id_contenido=objContenidoActual, id_fase__in=[2, 3, 4]).order_by('orden')
        dictActividades = {}

        if listaObjContenidosFasesActividades:

            for ObjContenidosFasesActividades in listaObjContenidosFasesActividades:
                dictActividades[int(ObjContenidosFasesActividades.orden)] = ObjContenidosFasesActividades
            # end for.

            # obtener el id_fase de la actividad.
            response['id_fase'] = int(dictActividades[ordenActividadActual].id_fase.id_fase)
            response['ultimaSiglasActividad'] = dictActividades[ordenActividadActual].id_actividad.nombre_actividad[-2:]
            response['siglasActividad'] = dictActividades[ordenActividadActual].id_actividad.nombre_actividad

            if diferenciado:
                id_diferenciado = 1
            else:
                id_diferenciado = 0

            regAlumnoActividades = TblAlumnoActividades(rut_alumno=objAlumno[0], id_contenido_fase_actividad=dictActividades[ordenActividadActual], fecha_inicio=fecha_actual, intento=intento, diferenciado=id_diferenciado)
            try:
                regAlumnoActividades.save()
            except:
                response = {'estatus': 0, 'mensaje': 'error al guardar en la tabla tbl_alumno_actividades.'}

            if objAlumno[0].autonomo == 0:

                regPlan = TblPlan(rut_alumno=objAlumno[0], id_contenido_unidad=dictContenidoUnidad[int(objContenidoActual.id_contenido)], fecha_inicio=fecha_actual)
                try:
                    regPlan.save()
                except:
                    response = {'estatus': 0, 'mensaje': 'error al guardar en la tabla tbl_plan.'}

    return HttpResponse(json.dumps(response))

def iniciarActividadComp(request):

    response = {'estatus': 1, 'mensaje': ''}
    id_contenido_fase_actividad = request.POST['id_contenido_fase_actividad']
    intento = request.POST['intento']
    now = datetime.datetime.now()
    fecha_actual = now.strftime("%Y-%m-%d %H:%M:%S")
    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)
    if objAlumno:
        if objAlumno[0].id_producto.id_producto == 2:
            diferenciado = False
        else:
            diferenciado = True

        objContenidoFaseActividad = TblContenidosFasesActividades.objects.filter(id_contenido_fase_actividad=int(id_contenido_fase_actividad))

        if objContenidoFaseActividad:
            if diferenciado:
                tipoActividad=1
            else:
                tipoActividad=0
            regAlumnoActividades = TblAlumnoActividades(rut_alumno=objAlumno[0], id_contenido_fase_actividad=objContenidoFaseActividad[0], fecha_inicio=fecha_actual, intento=int(intento)+1, diferenciado=tipoActividad)
            try:
                regAlumnoActividades.save()
            except:
                response = {'estatus': 0, 'mensaje': 'error al guardar'}
        else:
            response = {'estatus': 0, 'mensaje': 'error al guardar, no existe la actividad'}
    else:
        response = {'estatus': 0, 'mensaje': 'error al guardar, no existe el rut del alumno'}

    return HttpResponse(json.dumps(response))

def complementariasUnidad(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    locale.setlocale(locale.LC_TIME, 'es_CL')  # permite que obtenga el lenguaje por defecto en español para mostrar nombre del mes en español.

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    nombreUnidades = {}
    ordenUnidad = {}
    listaContenidos = {}

    puntajeActividad = {}
    fechaFinActividad = {}
    intentoActividad = {}
    puntajeA3Contenido = {}

    primerSetActividades = {}  # pueden ser actividades de Recuperacion o nivel
    nombrePrimerSetActividades = {}
    clasePrimerSetActividades = {}

    segundoSetActividades = {}  # pueden ser actividades de Nivel o profundizacion
    nombreSegundoSetActividades = {}
    claseSegundoSetActividades = {}

    criterioPuntajeA3 = 80
    diferenciado = False

    if objAlumno[0].id_producto.id_producto == 2:
        criterioPuntajeA3 = 80
        diferenciado = False

    if objAlumno[0].id_producto.id_producto == 3:
        criterioPuntajeA3 = 50
        diferenciado = True

    if objAlumno[0].autonomo == 0:
        listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad', 'orden')

    if objAlumno[0].autonomo == 1:
        listaObjContenidoUnidad = TblPlanAutonomo.objects.filter(rut_alumno=objAlumno[0]).order_by('id_unidad__orden', 'orden')

    for objContenidoUnidad in listaObjContenidoUnidad:

        nombreUnidades[objContenidoUnidad.id_unidad.id_unidad] = objContenidoUnidad.id_unidad.nombre_unidad

        if objContenidoUnidad.id_unidad.orden not in listaContenidos:
            listaContenidos[objContenidoUnidad.id_unidad.orden] = []

        if diferenciado:
            contenidoDiferenciado = TblContenidos.objects.filter(id_padre=int(objContenidoUnidad.id_contenido.id_contenido))
            ordenUnidad[int(contenidoDiferenciado[0].id_contenido)] = int(objContenidoUnidad.id_unidad.orden)
            listaContenidos[objContenidoUnidad.id_unidad.orden].append(contenidoDiferenciado[0])
        else:
            ordenUnidad[int(objContenidoUnidad.id_contenido.id_contenido)] = int(objContenidoUnidad.id_unidad.orden)
            listaContenidos[objContenidoUnidad.id_unidad.orden].append(objContenidoUnidad.id_contenido)


    # consultar las actividades que ha realizado el alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).exclude(id_contenido_fase_actividad__id_fase__id_fase=1).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        ultimaActividadAlumno = listaObjAlumnoActividades.last()
        if int(ultimaActividadAlumno.diferenciado) == 1:
            if diferenciado:
                idContenidoActual = ultimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido
            else:
                idContenidoActual = ultimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_padre
        else:
            if diferenciado:
                objDiferenciado = TblContenidos.objects.filter(id_padre=int(ultimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido))
                idContenidoActual = objDiferenciado[0].id_contenido
            else:
                idContenidoActual = ultimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido

        ordenUnidadActual = ordenUnidad[idContenidoActual]

        for ObjAlumnoActividades in listaObjAlumnoActividades:

            if ObjAlumnoActividades.puntaje is not None and ObjAlumnoActividades.fecha_fin is not None:

                puntajeActividad[int(ObjAlumnoActividades.id_contenido_fase_actividad.id_actividad.id_actividad)] = str(ObjAlumnoActividades.puntaje) + "%"
                fechaFinActividad[int(ObjAlumnoActividades.id_contenido_fase_actividad.id_actividad.id_actividad)] = str(ObjAlumnoActividades.fecha_fin.strftime("%d de %B de %Y"))
                intentoActividad[int(ObjAlumnoActividades.id_contenido_fase_actividad.id_actividad.id_actividad)] = int(ObjAlumnoActividades.intento)

            if int(ObjAlumnoActividades.id_contenido_fase_actividad.id_actividad.id_tipo_actividad.id_tipo_actividad) == 1 and int(ObjAlumnoActividades.id_contenido_fase_actividad.id_fase.id_fase) == 4:

                id_contenido = 0

                if diferenciado and ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre is None:
                    objTblContenidosDiferenciado = TblContenidos.objects.filter(id_padre=int(ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_contenido))
                    id_contenido = int(objTblContenidosDiferenciado[0].id_contenido)

                if diferenciado and ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre is not None:
                    id_contenido = int(ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_contenido)

                if not diferenciado and ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre is None:
                    id_contenido = int(ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_contenido)

                if not diferenciado and ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre is not None:
                    id_contenido = int(ObjAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre)

                puntajeA3Contenido[id_contenido] = int(ObjAlumnoActividades.puntaje)


    else:
        # el alumno no tiene actividades, se encuentra enn la unidad 1.
        ordenUnidadActual = 1
    # end if

    # consultar las actividades de recuperacion , nivel o profundizacion [5,6,7].

    listaObjContenidosFasesActividades = TblContenidosFasesActividades.objects.filter(id_contenido__in=listaContenidos[ordenUnidadActual], id_fase__id_fase__in=[5, 6, 7]).order_by('id_contenido__id_contenido', 'orden')

    for objContenidoFaseActividad in listaObjContenidosFasesActividades:

        if int(objContenidoFaseActividad.id_contenido.id_contenido) not in primerSetActividades:
            primerSetActividades[objContenidoFaseActividad.id_contenido.id_contenido] = []

        if int(objContenidoFaseActividad.id_contenido.id_contenido) not in segundoSetActividades:
            segundoSetActividades[objContenidoFaseActividad.id_contenido.id_contenido] = []

        if int(objContenidoFaseActividad.id_contenido.id_contenido) not in puntajeA3Contenido:
            puntajeA3Contenido[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 1

        if puntajeA3Contenido[int(objContenidoFaseActividad.id_contenido.id_contenido)] < criterioPuntajeA3:

            nombrePrimerSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'Recuperación'
            nombreSegundoSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'Nivel'

            clasePrimerSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'bg-recuperacion'
            claseSegundoSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'bg-nivelescolar'

            if int(objContenidoFaseActividad.id_fase.id_fase) == 5:
                primerSetActividades[objContenidoFaseActividad.id_contenido.id_contenido].append(objContenidoFaseActividad)

            if int(objContenidoFaseActividad.id_fase.id_fase) == 6:
                segundoSetActividades[objContenidoFaseActividad.id_contenido.id_contenido].append(objContenidoFaseActividad)

        elif puntajeA3Contenido[int(objContenidoFaseActividad.id_contenido.id_contenido)] >= criterioPuntajeA3:

            nombrePrimerSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'Nivel'
            nombreSegundoSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'Profundización'

            clasePrimerSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'bg-nivelescolar'
            claseSegundoSetActividades[
                int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'bg-complentarias'

            if int(objContenidoFaseActividad.id_fase.id_fase) == 6:
                primerSetActividades[objContenidoFaseActividad.id_contenido.id_contenido].append(objContenidoFaseActividad)

            if int(objContenidoFaseActividad.id_fase.id_fase) == 7:
                segundoSetActividades[objContenidoFaseActividad.id_contenido.id_contenido].append(objContenidoFaseActividad)


    data = {
        'nombreUnidades': nombreUnidades,
        'listaContenidos': listaContenidos[ordenUnidadActual],
        'ordenUnidadActual': ordenUnidadActual,
        'puntajeActividad': puntajeActividad,
        'fechaFinActividad': fechaFinActividad,
        'intentoActividad': intentoActividad,
        'primerSetActividades': primerSetActividades,
        'nombrePrimerSetActividades': nombrePrimerSetActividades,
        'clasePrimerSetActividades': clasePrimerSetActividades,
        'segundoSetActividades': segundoSetActividades,
        'nombreSegundoSetActividades': nombreSegundoSetActividades,
        'claseSegundoSetActividades': claseSegundoSetActividades,
    }

    return render(request, 'ggalbas/complementariasUnidad.html', data)

def complementariasLibre(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    locale.setlocale(locale.LC_TIME, 'es_CL')

    nombreUnidades = {}
    listaTodosContenidos = []
    ordenUnidad = {}
    listaContenidosUnidad = {}
    puntajeActividad = {}
    fechaFinActividad = {}
    intentoActividad = {}
    puntajeA3Contenido = {}
    primerSetActividades = {}  # pueden ser actividades de Recuperacion o nivel
    nombrePrimerSetActividades = {}
    clasePrimerSetActividades = {}
    segundoSetActividades = {}  # pueden ser actividades de Nivel o Recuperacion
    nombreSegundoSetActividades = {}
    claseSegundoSetActividades = {}

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    criterioPuntajeA3 = 80

    if objAlumno[0].id_producto.id_producto == 2:
        criterioPuntajeA3 = 80
        diferenciado = False

    if objAlumno[0].id_producto.id_producto == 3:
        criterioPuntajeA3 = 50
        diferenciado = True


    if objAlumno[0].autonomo == 0:
        listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad__orden', 'orden')

    if objAlumno[0].autonomo == 1:
        listaObjContenidoUnidad = TblPlanAutonomo.objects.filter(rut_alumno=objAlumno[0]).order_by('id_unidad__orden', 'orden')


    for objContenidoUnidad in listaObjContenidoUnidad:

        nombreUnidades[objContenidoUnidad.id_unidad.id_unidad] = objContenidoUnidad.id_unidad.nombre_unidad
        if objContenidoUnidad.id_unidad.orden not in listaContenidosUnidad:
            listaContenidosUnidad[objContenidoUnidad.id_unidad.orden] = []
        if diferenciado:
            contenidoDiferenciado = TblContenidos.objects.filter(id_padre=int(objContenidoUnidad.id_contenido.id_contenido))
            ordenUnidad[int(contenidoDiferenciado[0].id_contenido)] = int(objContenidoUnidad.id_unidad.orden)
            listaTodosContenidos.append(contenidoDiferenciado[0])
            listaContenidosUnidad[objContenidoUnidad.id_unidad.orden].append(contenidoDiferenciado[0])
        else:
            ordenUnidad[int(objContenidoUnidad.id_contenido.id_contenido)] = int(objContenidoUnidad.id_unidad.orden)
            listaTodosContenidos.append(objContenidoUnidad.id_contenido)
            listaContenidosUnidad[objContenidoUnidad.id_unidad.orden].append(objContenidoUnidad.id_contenido)

    # consultar las actividades que ha realizado el alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        for objAlumnoActividades in listaObjAlumnoActividades:

            if objAlumnoActividades.puntaje is not None and objAlumnoActividades.fecha_fin is not None:

                puntajeActividad[int(objAlumnoActividades.id_contenido_fase_actividad.id_actividad.id_actividad)] = str(objAlumnoActividades.puntaje) + "%"
                fechaFinActividad[int(objAlumnoActividades.id_contenido_fase_actividad.id_actividad.id_actividad)] = str(objAlumnoActividades.fecha_fin.strftime("%d de %B de %Y"))
                intentoActividad[int(objAlumnoActividades.id_contenido_fase_actividad.id_actividad.id_actividad)] = int(objAlumnoActividades.intento)

                if int(objAlumnoActividades.id_contenido_fase_actividad.id_actividad.id_tipo_actividad.id_tipo_actividad) == 1 and int(objAlumnoActividades.id_contenido_fase_actividad.id_fase.id_fase) == 4:

                    id_contenido = 0

                    if diferenciado and objAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre is None:
                        objTblContenidosDiferenciado = TblContenidos.objects.filter(id_padre=int(objAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_contenido))
                        id_contenido = int(objTblContenidosDiferenciado[0].id_contenido)

                    if diferenciado and objAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre is not None:
                        id_contenido = int(objAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_contenido)

                    if not diferenciado and objAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre is None:
                        id_contenido = int(objAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_contenido)

                    if not diferenciado and objAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre is not None:
                        id_contenido = int(objAlumnoActividades.id_contenido_fase_actividad.id_contenido.id_padre)

                    puntajeA3Contenido[id_contenido] = int(objAlumnoActividades.puntaje)



    # consultar todas las actividades de recuperacion , nivel o profundizacion fases: [5,6,7]
    listaObjContenidosFasesActividades = TblContenidosFasesActividades.objects.filter(id_contenido__in=listaTodosContenidos, id_fase__id_fase__in=[5, 6, 7]).order_by('id_contenido__id_contenido', 'orden')

    for objContenidoFaseActividad in listaObjContenidosFasesActividades:

        if int(objContenidoFaseActividad.id_contenido.id_contenido) not in primerSetActividades:
            primerSetActividades[objContenidoFaseActividad.id_contenido.id_contenido] = []

        if int(objContenidoFaseActividad.id_contenido.id_contenido) not in segundoSetActividades:
            segundoSetActividades[objContenidoFaseActividad.id_contenido.id_contenido] = []

        # Si no existe evaluaciones A3 para el contenido, entonces asignar puntaje menor a 80 de tal forma mostrar fase de recuperacion y nivel.
        if int(objContenidoFaseActividad.id_contenido.id_contenido) not in puntajeA3Contenido:
            puntajeA3Contenido[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 1

        # Si el puntaje de la evaluacion de nivel es menor de 80, muestra actividades de recuperacion y nivel.
        if puntajeA3Contenido[int(objContenidoFaseActividad.id_contenido.id_contenido)] < criterioPuntajeA3:

            nombrePrimerSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'Recuperación'
            nombreSegundoSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'Nivel'
            clasePrimerSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'bg-recuperacion'
            claseSegundoSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'bg-nivelescolar'

            if int(objContenidoFaseActividad.id_fase.id_fase) == 5:
                primerSetActividades[objContenidoFaseActividad.id_contenido.id_contenido].append(objContenidoFaseActividad)

            if int(objContenidoFaseActividad.id_fase.id_fase) == 6:
                segundoSetActividades[objContenidoFaseActividad.id_contenido.id_contenido].append(objContenidoFaseActividad)

        # Si el puntaje de la evaluacion de nivel es mayor de 80, muestra actividades de nivel y profundizacion.
        elif puntajeA3Contenido[int(objContenidoFaseActividad.id_contenido.id_contenido)] >= criterioPuntajeA3:

            nombrePrimerSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'Nivel'
            nombreSegundoSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'Profundización'
            clasePrimerSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'bg-nivelescolar'
            claseSegundoSetActividades[int(objContenidoFaseActividad.id_contenido.id_contenido)] = 'bg-complentarias'

            if int(objContenidoFaseActividad.id_fase.id_fase) == 6:
                primerSetActividades[objContenidoFaseActividad.id_contenido.id_contenido].append(objContenidoFaseActividad)

            if int(objContenidoFaseActividad.id_fase.id_fase) == 7:
                segundoSetActividades[objContenidoFaseActividad.id_contenido.id_contenido].append(objContenidoFaseActividad)


    data = {
        'nombreUnidades': nombreUnidades,
        'listaContenidosUnidad': listaContenidosUnidad,
        'puntajeActividad': puntajeActividad,
        'fechaFinActividad': fechaFinActividad,
        'intentoActividad': intentoActividad,
        'primerSetActividades': primerSetActividades,
        'nombrePrimerSetActividades': nombrePrimerSetActividades,
        'clasePrimerSetActividades': clasePrimerSetActividades,
        'segundoSetActividades': segundoSetActividades,
        'nombreSegundoSetActividades': nombreSegundoSetActividades,
        'claseSegundoSetActividades': claseSegundoSetActividades,
    }

    return render(request, 'ggalbas/complementariasLibre.html', data)

def validarUnidadSigHabilitada(request):

    response = {'estatus': 1, 'mensaje': ''}

    # parametros enviados por POST.
    ordenUnidadActual = request.POST["ordenUnidadActual"]

    objAlumno = TblAlumnos.objects.filter(rut_alumno=request.session['rut'])
    autonomo = int(objAlumno[0].autonomo)
    opcionActivarUnidades = int(objAlumno[0].codigo_lista.activar_unidades)

    # verificar si la siguiente unidad se encuentra habilitada por el tutor.
    listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista, id_unidad__orden=int(ordenUnidadActual) + 1).order_by('orden')

    total_contenidos_activos = 0
    total_contenidos = len(listaObjContenidoUnidad)

    for ObjContenidoUnidad in listaObjContenidoUnidad:
        total_contenidos_activos += int(ObjContenidoUnidad.activo)

    response['total_contenidos'] = total_contenidos
    response['total_contenidos_activos'] = total_contenidos_activos
    response['opcionActivarUnidades'] = opcionActivarUnidades
    response['autonomo'] = autonomo
    return HttpResponse(json.dumps(response))

def validarActividadComplementariaIniciada(request):

    response = {'estatus': 1, 'mensaje': ''}

    locale.setlocale(locale.LC_TIME, '')  # permite que obtenga el lenguaje por defecto en español para mostrar nombre del mes en español.
    # parametros de sesion.
    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    response['id_alumno_actividad'] = 0
    response['id_contenido_fase_actividad'] = ''
    response['intento'] = ''
    response['nombreContenido'] = ''
    response['nombreTipoAct'] = ''
    response['siglasAct'] = ''
    response['ultimoPuntaje'] = ''
    response['fechaUltimoPuntaje'] = ''

    # consulta las actividades del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase__in=[5, 6, 7]).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()

        if objUltimaActividadAlumno.puntaje is None or objUltimaActividadAlumno.fecha_fin is None:

            # si tiene una actividad iniciada.
            response['id_alumno_actividad'] = int(objUltimaActividadAlumno.id_alumno_actividad)
            response['id_contenido_fase_actividad'] = int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido_fase_actividad)
            response['intento'] = int(objUltimaActividadAlumno.intento)
            response['nombreContenido'] = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.descripcion
            response['nombreTipoAct'] = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_tipo_actividad.nombre_tipo
            response['siglasAct'] = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad.strip()

            # buscar la ultima vez que realizo la actividad.
            for registro in listaObjAlumnoActividades:
                if int(registro.id_contenido_fase_actividad.id_actividad.id_actividad) == int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_actividad):
                    if registro.fecha_fin is not None and registro.puntaje is not None:
                        response['ultimoPuntaje'] = str(registro.puntaje) + "%"
                        response['fechaUltimoPuntaje'] = str(registro.fecha_fin.strftime("%d de %B de %Y"))
                    # end if.
                # end if.
            # end for.

    return HttpResponse(json.dumps(response))

def validarAlumnoCompLibre(request):

    # verificar si el alumno tiene una actividad complementaria iniciada.
    # retorna estatus = 1 si el alumno no ha iniciado ninguna actividad.
    # retorna estatus = 2 si el alumno ya ha iniciado alguna actividad, devuelve la informacion de dicha actividad.

    locale.setlocale(locale.LC_TIME, '')  # permite que obtenga el lenguaje por defecto en español para mostrar nombre del mes en español.

    rutAlumno = request.session['rut']

    response = {'estatus': 1, 'mensaje': ''}

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    if objAlumno:

        # Consultar los contenidos de la unidades
        listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad__orden', 'orden')
        unidadPorContenido = {}
        if listaObjContenidoUnidad:

            for ObjContenidoUnidad in listaObjContenidoUnidad:
                unidadPorContenido[int(ObjContenidoUnidad.id_contenido.id_contenido)] = int(ObjContenidoUnidad.id_unidad.orden)
            # end for.

        listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase__in=[5, 6, 7]).order_by('fecha_inicio')

        if listaObjAlumnoActividades:

            objUltimaActividadAlumno = listaObjAlumnoActividades.last()

            if objUltimaActividadAlumno.puntaje is None or objUltimaActividadAlumno.fecha_fin is None:
                response['estatus'] = 2
                response['mensaje'] = 'el alumno tiene una actividad iniciada que aun no ha terminado.'
                # datos de la actividad.
                response['nombreContenido'] = objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.descripcion
                response['nombreTipoAct'] = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_tipo_actividad.nombre_tipo
                response['siglasAct'] = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad
                response['ultimoPuntaje'] = ''
                response['fechaUltimoPuntaje'] = ''
                response['unidadIniciada'] = unidadPorContenido[int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido)]

                # Encontrar la ultima vez que realize la actividad , si es que algun momento la hizo.
                for registro in listaObjAlumnoActividades:
                    if int(registro.id_contenido_fase_actividad.id_actividad.id_actividad) == int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_actividad):
                        if registro.fecha_fin is not None and registro.puntaje is not None:
                            response['ultimoPuntaje'] = str(registro.puntaje) + "%"
                            response['fechaUltimoPuntaje'] = str(registro.fecha_fin.strftime("%d de %B de %Y"))
                        # end if
                    # end if
                # end for.
            # end if
    else:
        response['estatus'] = 0
        response['mensaje'] = 'El rut del alumno no existe, intente de nuevo.'

    return HttpResponse(json.dumps(response))

def validarContenidoTerminado(request):

    # verificar si el alumno aun tiene actividades por realizar en su contenido.
    # retorna estatus = 1 si no tiene mas actividades en el contenido.
    # retorna estatus = 2 si aun tiene actividades en el contenido.

    response = {'estatus': 1, 'mensaje': ''}

    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    if objAlumno:
        # Consultar los contenidos de la unidades
        listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad__orden', 'orden')

        listaContenidos = []

        if listaObjContenidoUnidad:

            for ObjContenidoUnidad in listaObjContenidoUnidad:
                listaContenidos.append(ObjContenidoUnidad.id_contenido)
            # end for.

            # consultar la ultima actividad finalizada por el alumno.
            listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_contenido__in=listaContenidos, id_contenido_fase_actividad__id_fase__id_fase__in=[2, 3, 4], puntaje__isnull=False, fecha_fin__isnull=False).order_by('fecha_inicio')

            if listaObjAlumnoActividades:

                objUltimaActividadAlumno = listaObjAlumnoActividades.last()

                if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_tipo_actividad.id_tipo_actividad) == 1 \
                        and int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase) == 4 \
                        and ((int(objUltimaActividadAlumno.intento) == 1 and int(objUltimaActividadAlumno.puntaje) >= 65)
                             or (int(objUltimaActividadAlumno.intento) == 2 and int(objUltimaActividadAlumno.puntaje) >= 50)
                             or int(objUltimaActividadAlumno.intento) == 3):

                    response = {'estatus': 1, 'mensaje': 'no hay mas actividades en el contenido. '}
                else:
                    response = {'estatus': 2, 'mensaje': 'aun quedan actividades en el contenido.'}
                # end if.
            else:
                response = {'estatus': 2, 'mensaje': 'aun quedan actividades en el contenido.'}
        else:
            response = {'estatus': 0, 'mensaje': 'no se encontraron los contenidos en tabla tbl_contenido_unidad.'}
    else:
        response = {'estatus': 0, 'mensaje': 'no se encontro el rut del alumno.'}

    return HttpResponse(json.dumps(response))

def visorActividad(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)
    if objAlumno:

        listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).order_by('fecha_inicio')
        if listaObjAlumnoActividades:
            ultimaActividadAlumno = listaObjAlumnoActividades.last()

            if objAlumno[0].id_producto.id_producto == 3:
                actividadDiferenciada = TblActividades.objects.filter(id_padre=int(ultimaActividadAlumno.id_contenido_fase_actividad.id_actividad.id_actividad))
                actividad = actividadDiferenciada[0]
            else:
                actividad = ultimaActividadAlumno.id_contenido_fase_actividad.id_actividad

            objContenidoFaseActividad = ultimaActividadAlumno.id_contenido_fase_actividad
        else:
            return HttpResponse('No se encontraron actividad para el rut del alumno, intente de nuevo.')
    else:
        return HttpResponse('El rut del alumno no existe , intente de nuevo.')
    data = {
        'objContenidoFaseActividad': objContenidoFaseActividad,
        'actividad':actividad
    }

    return render(request, 'ggalbas/visorActividad.html', data)

def visorActividadComp(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('index')

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).order_by('fecha_inicio')

    objUltimaActividadAlumno = listaObjAlumnoActividades.last()

    data = {
        'objContenidoFaseActividad': objUltimaActividadAlumno.id_contenido_fase_actividad
    }

    return render(request, 'ggalbas/visorActividadComp.html', data)

def obtenerIp(request):
    host = socket.gethostname()
    ip = socket.gethostbyname(host)
    return HttpResponse(ip)

def redondeo(x):
    return int(x + math.copysign(0.5, x))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def ultimasSiglas(nombre_actividad):
    return nombre_actividad.strip()[-2:]

def proximo_dia_semana(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)
