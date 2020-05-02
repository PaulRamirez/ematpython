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

from ggalbas.models import TblAlumnos, TblListas, TblPreguntausuarios, TblSubproducto, TblRegistroipAlumno, TblNiveles, \
    TblInstituciones, TblActividades, TblTipoActividad, TblAlumnoActividades, TblAlumnoRespuestas, TblPreguntas, \
    TblHabilidades, TblEje, TblAlumnoDiagnostico, TblContenidoUnidad, TblPlanAutonomo, TblUnidades, TblContenidosFasesActividades, \
    TblContenidos, TblFases, TblPlan, TblAlumnoRespuestasActividad
from core.models import Preguntas2Basico, Pruebas, PreguntasInstancias, Guias, Preguntas2BasicoMateriales, PreguntasInstanciasMateriales

from core.views import flagPais, obtenerSubdominio

def portadaInicialMT(request):
    return render(request, 'visores/portadaInicialMT.html')

def visorMT(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('/ggalbas/index')

    # nombre de la base de datos del MT.
    db = 'e_test'

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase__in=[2, 3, 4]).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        objActividad = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad

        # si el campo prueba_guia esta vacio , busca la prueba en e_test  y actualiza los campos.
        if objActividad.prueba_guia is None:

            objPruebas = Pruebas.objects.using(db).filter(codprueba=objActividad.nombre_actividad)
            if objPruebas:
                objActividad.prueba_guia = int(objPruebas[0].idprueba)
                objActividad.descripcion_actividades = objPruebas[0].descprueba
                objActividad.npreguntas = int(objPruebas[0].npreguntas)
                try:
                    objActividad.save()
                except:
                    return HttpResponse('error al actualizar la tabla tbl_actividades')
            else:
                return HttpResponse('error, no existe la prueba en base de datos e_test.')
        # end if.

        pruebaGuia = int(objActividad.prueba_guia)

        # consulta las respuestas del alumno.

        objAlumnoRespuesta = TblAlumnoRespuestas.objects.filter(rut_alumno=objAlumno[0].rut_alumno, prueba_guia=pruebaGuia)


        if objAlumnoRespuesta:
            npregunta = int(objAlumnoRespuesta.last().npregunta)
        else:
            npregunta = 0

        # consulta los datos de la pregunta actual
        listaPreguntas2Basico = Preguntas2Basico.objects.using(db).filter(idprueba=pruebaGuia)
        total_ejercicios = len(listaPreguntas2Basico)

        if npregunta == total_ejercicios:
            return redirect('portadaFinalMT')
        # end if.

        posiciones = str(listaPreguntas2Basico[npregunta].posiciones_botones)
        pos_boton = posiciones.replace('!', "")
        lista_pos = pos_boton.split(',')
        posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]

        npreg = listaPreguntas2Basico[npregunta].npregunta                        # numero de la pregunta.
        imagen_ejercicio = base64.b64encode(listaPreguntas2Basico[npregunta].imagen).decode()  # imagen de la pregunta.
        tipo_ejercicio = listaPreguntas2Basico[npregunta].tipo_ejercicio           # tipo de pregunta.
        num_campos_completar = listaPreguntas2Basico[npregunta].num_campos_completar

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
            'id_alumno_actividad': objUltimaActividadAlumno.id_alumno_actividad,
            'nombre_actividad': objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad,
            'total_ejercicios': total_ejercicios,
            'imagen_ejercicio': imagen_ejercicio,
            'botones': posicion_boton,
            'npregunta': npreg,
            'tipo_ejercicio': tipo_ejercicio,
            'num_campos_completar': num_campos_completar,
            'alternativa': alternativa
        }

    return render(request, 'visores/visorMT.html', data)

def guardaRespuestaMT(request):

    # parametros de sesion.
    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    response = {'estatus': 1, 'mensaje': ''}

    bd = 'e_test'

    # fecha actual
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    # parametros enviados por POST.
    id_alumno_actividad = request.POST['id_alumno_actividad']
    npregunta = int(request.POST['npregunta'])
    tipo_ejercicio = int(request.POST['tipo_ejercicio'])
    num_campos_completar = int(request.POST['num_campos_completar'])
    respuestaAlumno = request.POST['respuestaAlumno']

    # consultar la ultima actividad del alumno.
    objTblAlumnoActividades = TblAlumnoActividades.objects.filter(id_alumno_actividad=id_alumno_actividad)
    pruebaGuia = int(objTblAlumnoActividades[0].id_contenido_fase_actividad.id_actividad.prueba_guia)

    # Consulta la respuesta correcta de la pregunta.
    objPreguntasInstancias = PreguntasInstancias.objects.using(bd).filter(idprueba=pruebaGuia, npregunta=npregunta)

    respuesta_pregunta = objPreguntasInstancias[0].respuesta_pregunta
    aprobada = 0

    if tipo_ejercicio == 1:  # ejercicios de tipo fill

        cantidadRespuestasCorrectas = 0
        listaRespuestas = respuesta_pregunta.split(sep='~')
        listaRespuestaAlumno = respuestaAlumno.split(sep='~')

        for x in range(num_campos_completar):
            if listaRespuestas[x] == listaRespuestaAlumno[x]:
                cantidadRespuestasCorrectas += 1
        # end for.

        aprobada = int(cantidadRespuestasCorrectas) / num_campos_completar

    elif tipo_ejercicio == 2:  # ejercicios de tipo seleccion simple.

        if respuesta_pregunta == respuestaAlumno:
            aprobada = 1
        else:
            aprobada = 0

    elif tipo_ejercicio == 3:  # ejercicios de tipo seleccion multiple.

        listaRespuestas = respuesta_pregunta.replace('~', ",").split(sep=',')

        if listaRespuestas[0] == respuestaAlumno:
            aprobada = 1
        else:
            aprobada = 0


    # guarda la respuesta del alumno.
    registroRespuesta = TblAlumnoRespuestas(rut_alumno=objTblAlumnoActividades[0].rut_alumno, npregunta=npregunta, prueba_guia=pruebaGuia, respuesta_alumno=respuestaAlumno, aprobada=aprobada, fecha=fechaActual)

    try:
        registroRespuesta.save()
    except:
        response = {'estatus': 0, 'mensaje': 'error al guardar en la tabla tbl_alumno_respuestas'}

    return HttpResponse(json.dumps(response))

def portadaFinalMT(request):

    # parametros de sesion.
    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    # fecha actual
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")
    db = 'e_test'

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase=2).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        objActividadAlumno = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad

        if objUltimaActividadAlumno.puntaje is None and objUltimaActividadAlumno.fecha_fin is None:

            pruebaGuia = int(objActividadAlumno.prueba_guia)

            # consulta total de preguntas.
            Totalpreguntas = len(Preguntas2Basico.objects.using(db).filter(idprueba=pruebaGuia))

            #  consultar las respuestas del alumno.
            listaTblAlumnoRespuestas = TblAlumnoRespuestas.objects.filter(rut_alumno=objAlumno[0], prueba_guia=pruebaGuia)

            puntajePreguntas = 0
            if listaTblAlumnoRespuestas:
                for objTblAlumnoRespuestas in listaTblAlumnoRespuestas:
                    puntajePreguntas += int(objTblAlumnoRespuestas.aprobada)
            # end if.

            puntajeActividad = (puntajePreguntas / Totalpreguntas) * 100

            # si el puntaje de la actividad es cero, se sustituye por 1.
            if puntajeActividad == 0:
                puntajeActividad = 1

            objUltimaActividadAlumno.puntaje = redondeo(puntajeActividad)
            objUltimaActividadAlumno.fecha_fin = fechaActual

            try:
                objUltimaActividadAlumno.save()
            except:
                print('error al actualizar el puntaje de la actividad')

    data = {
        'nombre_actividad': objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad,
        'puntaje': objUltimaActividadAlumno.puntaje,
    }

    return render(request, 'visores/portadaFinalMT.html', data)

def portadaInicialAprendizaje(request):
    return render(request, 'visores/portadaInicialAprendizaje.html')

def visorAprendizaje(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('/ggalbas/index')

    # nombre de la base de datos donde se encuentra la actividad.
    db = 'materiales'

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    libre = int(objAlumno[0].libre)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).exclude(id_contenido_fase_actividad__id_fase__id_fase=1).order_by('fecha_inicio')

    objUltimaActividadAlumno = listaObjAlumnoActividades.last()

    id_fase = int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase)

    objActividad = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad

    # si el campo prueba_guia esta vacio , busca la actividad en materiales  y actualiza los campos.
    if objActividad.prueba_guia is None:

        objGuias = Guias.objects.using(db).filter(codguia=objActividad.nombre_actividad)
        if objGuias:
            objActividad.prueba_guia = int(objGuias[0].idguia)
            objActividad.descripcion_actividades = objGuias[0].descguia
            objActividad.npreguntas = int(objGuias[0].npreguntas)
            try:
                objActividad.save()
            except:
                return HttpResponse('error al actualizar la tabla tbl_actividades')

    # end if.

    # consulta las respuestas del alumno.
    ultimaRespuesta = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objUltimaActividadAlumno).order_by('-fecha')

    if ultimaRespuesta:
        npregunta = int(ultimaRespuesta[0].npregunta)
        intento = int(ultimaRespuesta[0].intento)
        aprobada = int(ultimaRespuesta[0].aprobada)

    else:
        npregunta = 1
        intento = 0
        aprobada = 0

    listaPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(db).filter(idguia=int(objActividad.prueba_guia))

    total_ejercicios = len(listaPreguntas2BasicoMateriales)
    tipoEjercicio = listaPreguntas2BasicoMateriales[npregunta-1].tipo_ejercicio
    numeroCamposCompletar = listaPreguntas2BasicoMateriales[npregunta-1].num_campos_completar

    if tipoEjercicio == 1:  # ejercicio tipo fill
        maximo_intento = 3

    elif tipoEjercicio == 2:  # ejercicio de seleccion unica.

        if numeroCamposCompletar <= 4:
            maximo_intento = numeroCamposCompletar - 1
        else:
            maximo_intento = 3
        # end if.

    elif tipoEjercicio == 3:   # ejercicio de seleccion multiple.

        maximo_intento = 3
    else:
        maximo_intento = 3      # por defecto maximo 3 intentos.
    # end if.


    if (aprobada == 1) or (intento == maximo_intento):
        if npregunta == total_ejercicios:
            return redirect('portadaFinalAprendizaje')
        else:
            npregunta = npregunta + 1


    posiciones = str(listaPreguntas2BasicoMateriales[npregunta-1].posiciones_botones)
    pos_boton = posiciones.replace('!', "")
    lista_pos = pos_boton.split(',')
    posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]
    img = base64.b64encode(listaPreguntas2BasicoMateriales[npregunta-1].imagen).decode()
    tipoEjercicio = listaPreguntas2BasicoMateriales[npregunta-1].tipo_ejercicio
    num_campos_completar = listaPreguntas2BasicoMateriales[npregunta-1].num_campos_completar

    alternativa = {1: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa1),
                   2: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa2),
                   3: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa3),
                   4: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa4),
                   5: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa5),
                   6: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa6),
                   7: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa7),
                   8: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa8)
                   }

    url_boton_volver = ''

    if libre == 0 and (id_fase == 3 or id_fase == 4):
        url_boton_volver = 'contenidosAlumno'

    if libre == 0 and (id_fase == 5 or id_fase == 6 or id_fase == 7):
        url_boton_volver = 'complementariasUnidad'

    if libre == 1 and (id_fase == 5 or id_fase == 6 or id_fase == 7):
        url_boton_volver = 'complementariasLibre'

    data = {
        'id_alumno_actividad': objUltimaActividadAlumno.id_alumno_actividad,
        'nombre_actividad': objActividad.nombre_actividad,
        'total_ejercicios': total_ejercicios,
        'npregunta': npregunta,
        'tipoEjercicio': tipoEjercicio,
        'num_campos_completar': num_campos_completar,
        'img': img,
        'botones': posicion_boton,
        'alternativa': alternativa,
        'url_boton_volver': url_boton_volver
    }

    return render(request, 'visores/visorAprendizaje.html', data)

def guardaRespuestaVisorAprendizaje(request):

    response = {'estatus': 1, 'mensaje': ''}

    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    # fecha actual
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    # parametros enviados por POST.
    id_alumno_actividad = request.POST['id_alumno_actividad']
    npregunta = int(request.POST['npregunta'])
    tipo_ejercicio = int(request.POST['tipo_ejercicio'])
    num_campos_completar = int(request.POST['num_campos_completar'])
    respuestasAlumno = request.POST['respuestasAlumno']


    # nombre de la base de datos de la actividad.
    bd = 'materiales'

    # consultar la ultima actividad del alumno.
    objTblAlumnoActividades = TblAlumnoActividades.objects.filter(id_alumno_actividad=id_alumno_actividad)
    pruebaGuia=int(objTblAlumnoActividades[0].id_contenido_fase_actividad.id_actividad.prueba_guia)

    # consulta las respuestas del alumno.
    objTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objTblAlumnoActividades[0], npregunta=npregunta).order_by('-fecha')

    if objTblAlumnoRespuestasActividad:
        intento = int(objTblAlumnoRespuestasActividad[0].intento) + 1

    else:
        intento = 1

    # consultar Tipo de ejercicio y cantidad de alternativas.
    objPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=pruebaGuia, npregunta=npregunta)

    if objPreguntas2BasicoMateriales[0].solucion_imagen is None:
        solucion_imagen = ''
    else:
        solucion_imagen = base64.b64encode(objPreguntas2BasicoMateriales[0].solucion_imagen).decode()

    # Consulta la Respuesta correcta
    objPreguntasInstanciasMateriales = PreguntasInstanciasMateriales.objects.using(bd).filter(idguia=pruebaGuia, npregunta=npregunta)

    respuesta_correcta = objPreguntasInstanciasMateriales[0].respuesta_pregunta


    if tipo_ejercicio == 1:  # ejercicio tipo fill

        maximo_intento = 3

        cantidadRespuestasCorrectas = 0
        listaRespuestasAlumno = respuestasAlumno.split(sep='~')
        listaRespuestaCorrecta = respuesta_correcta.split(sep='~')
        listaCondicionFill = []

        for x in range(num_campos_completar):
            if listaRespuestaCorrecta[x] == listaRespuestasAlumno[x]:
                cantidadRespuestasCorrectas += 1
                listaCondicionFill.append('correcto')
            else:
                listaCondicionFill.append('incorrecto')
        # end for.

        aprobada = cantidadRespuestasCorrectas / num_campos_completar


    elif tipo_ejercicio == 2:  # ejercicio de seleccion unica.

        if respuesta_correcta == respuestasAlumno:
            aprobada = 1
        else:
            aprobada = 0

        if num_campos_completar <= 4:
            maximo_intento = num_campos_completar - 1
        else:
            maximo_intento = 3
        # end if.


    elif tipo_ejercicio == 3:  # ejercicio de seleccion multiple.

        maximo_intento = 3

        listaRespuestas = respuesta_correcta.replace('~', ",").split(sep=',')

        if listaRespuestas[0] == respuestasAlumno:
            aprobada = 1
        else:
            aprobada = 0
    else:
        maximo_intento = 3
    # end if.

    # guarda la respuesta  del alumno.
    registroRespuesta = TblAlumnoRespuestasActividad(id_alumno_actividad=objTblAlumnoActividades[0], npregunta=npregunta, respuesta_alumno=respuestasAlumno, fecha=fechaActual, aprobada=aprobada, intento=intento, nvuelta=1, prueba_guia=pruebaGuia)

    try:
        registroRespuesta.save()
    except:
        response = {'estatus': 0, 'mensaje': 'error al guardar en la tabla tbl_alumno_respuestas_actividad'}

    response['aprobada'] = aprobada

    if aprobada == 1 or intento == maximo_intento:
        response['solucion_imagen'] = solucion_imagen
    # end if.

    if intento < maximo_intento:    # tiene mas intentos?
        response['TieneMasIntentos'] = 'SI'

        if tipo_ejercicio == 1:     # es un ejercicio tipo fill?.
            response['listaCondicionFill'] = listaCondicionFill
        # end if.

    else:
        response['TieneMasIntentos'] = 'NO'
        response['respuesta_correcta'] = respuesta_correcta
    # end if

    return HttpResponse(json.dumps(response))

def portadaFinalAprendizaje(request):

    # fecha actual
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    bd = 'materiales'

    # parametros de sesion.
    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    objTblAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).order_by('-fecha_inicio')

    libre = int(objAlumno[0].libre)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).exclude(id_contenido_fase_actividad__id_fase__id_fase=1).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        id_fase = objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase
        ultimaRespuesta = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objTblAlumnoActividades[0]).order_by('-fecha')

        if ultimaRespuesta:
            pruebaGuiaActual = int(ultimaRespuesta[0].prueba_guia)
            if int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.prueba_guia) == pruebaGuiaActual:
                objActividadAlumno = TblActividades.objects.filter(prueba_guia=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.prueba_guia))
            else:
                objActividadAlumno = TblActividades.objects.filter(prueba_guia=pruebaGuiaActual)

        # si no lo inicio se inicia el MT correspondiente a su subproducto
        else:
            objActividadAlumno = TblActividades.objects.filter(prueba_guia=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.prueba_guia))

        if objUltimaActividadAlumno.puntaje is None and objUltimaActividadAlumno.fecha_fin is None:

            # consultar total de preguntas de la actividad y tipo de pregunta
            listaPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=int(objActividadAlumno[0].prueba_guia))
            Totalpreguntas = 0
            tipoEjercicio = {}
            if listaPreguntas2BasicoMateriales:
                Totalpreguntas = len(listaPreguntas2BasicoMateriales)
                for objPreguntas2BasicoMateriales in listaPreguntas2BasicoMateriales:
                    tipoEjercicio[int(objPreguntas2BasicoMateriales.npregunta)] = int(objPreguntas2BasicoMateriales.tipo_ejercicio)
                # end for.
            # end if.

            intentosPregunta = {}
            puntajeParcialFill = {}
            puntajeFinalAlternativaUnica = {}
            puntajeFinalAlternativaMultiple = {}
            listaPreguntas = []

            listaTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objUltimaActividadAlumno).order_by('npregunta', 'intento')

            if listaTblAlumnoRespuestasActividad:

                for objTblAlumnoRespuestasActividad in listaTblAlumnoRespuestasActividad:

                    if int(objTblAlumnoRespuestasActividad.npregunta) not in listaPreguntas:
                        listaPreguntas.append(int(objTblAlumnoRespuestasActividad.npregunta))

                    intentosPregunta[int(objTblAlumnoRespuestasActividad.npregunta)] = int(objTblAlumnoRespuestasActividad.intento)

                    if tipoEjercicio[int(objTblAlumnoRespuestasActividad.npregunta)] == 1:  # ejercicio tipo fill.

                        if int(objTblAlumnoRespuestasActividad.npregunta) not in puntajeParcialFill:
                            puntajeParcialFill[int(objTblAlumnoRespuestasActividad.npregunta)] = 0
                        # end if.
                        puntajeParcialFill[int(objTblAlumnoRespuestasActividad.npregunta)] += float(objTblAlumnoRespuestasActividad.aprobada)

                    elif tipoEjercicio[int(objTblAlumnoRespuestasActividad.npregunta)] == 2:  # ejercicio tipo seleccion unica.
                        puntajeFinalAlternativaUnica[int(objTblAlumnoRespuestasActividad.npregunta)] = int(objTblAlumnoRespuestasActividad.aprobada)

                    elif tipoEjercicio[int(objTblAlumnoRespuestasActividad.npregunta)] == 3:  # ejercicio tipo seleccion multiple.
                        puntajeFinalAlternativaMultiple[int(objTblAlumnoRespuestasActividad.npregunta)] = int(objTblAlumnoRespuestasActividad.aprobada)
                    # end if.
                # end for.

                puntajePreguntas = 0
                # finalmente volver a recorrer las preguntas para calculos finales.
                for npregunta in listaPreguntas:

                    if tipoEjercicio[npregunta] == 1:  # ejercicio tipo fill.
                        puntajePreguntas += (puntajeParcialFill[npregunta] / intentosPregunta[npregunta])

                    elif tipoEjercicio[npregunta] == 2:  # ejercicio tipo seleccion unica.
                        puntajePreguntas += (puntajeFinalAlternativaUnica[npregunta] / intentosPregunta[npregunta])

                    elif tipoEjercicio[npregunta] == 3:  # ejercicio tipo seleccion multiple.
                        puntajePreguntas += (puntajeFinalAlternativaMultiple[npregunta] / intentosPregunta[npregunta])
                    # end if.

                # end for.

                puntajeActividad = redondeo((puntajePreguntas / Totalpreguntas) * 100)

                # si el puntaje de la actividad es cero, se sustituye por 1.
                if puntajeActividad == 0:
                    puntajeActividad = 1
                # end if.

                objUltimaActividadAlumno.puntaje = puntajeActividad
                objUltimaActividadAlumno.fecha_fin = fechaActual
                try:
                    objUltimaActividadAlumno.save()
                except:
                    response = {'estatus': 0, 'mensaje': 'error al actualizar en la tabla tbl_alumno_actividades'}

            # end if.

    url_boton = ''

    if libre == 0 and (id_fase == 3 or id_fase == 4):
        url_boton = 'contenidosAlumno'

    if libre == 0 and (id_fase == 5 or id_fase == 6 or id_fase == 7):
        url_boton = 'complementariasUnidad'

    if libre == 1 and (id_fase == 5 or id_fase == 6 or id_fase == 7):
        url_boton = 'complementariasLibre'

    data = {
        'nombre_actividad': objActividadAlumno[0].nombre_actividad,
        'puntaje': objUltimaActividadAlumno.puntaje,
        'url_boton': url_boton
    }

    return render(request, 'visores/portadaFinalAprendizaje.html', data)

def portadaInicialRepaso(request):
    return render(request, 'visores/portadaInicialRepaso.html')

def visorRepaso(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('/ggalbas/index')

    # nombre de la base de datos donde se encuentra la actividad.
    db = 'materiales'

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).exclude(id_contenido_fase_actividad__id_fase__id_fase=1).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        objActividad = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad

        # si el campo prueba_guia esta vacio , busca la actividad en materiales  y actualiza los campos.
        if objActividad.prueba_guia is None:

            objGuias = Guias.objects.using(db).filter(codguia=objActividad.nombre_actividad)

            if objGuias:
                objActividad.prueba_guia = int(objGuias[0].idguia)
                objActividad.descripcion_actividades = objGuias[0].descguia
                objActividad.npreguntas = int(objGuias[0].npreguntas)
                try:
                    objActividad.save()
                except:
                    print('error al actualizar los datos de la actividad')

        # consulta las respuestas del alumno.
        objTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objUltimaActividadAlumno, prueba_guia=int(objActividad.prueba_guia))

        if objTblAlumnoRespuestasActividad:
            npregunta = int(objTblAlumnoRespuestasActividad.last().npregunta)
            intento = int(objTblAlumnoRespuestasActividad.last().intento)
            aprobada = int(objTblAlumnoRespuestasActividad.last().aprobada)
        else:
            npregunta = 1
            intento = 0
            aprobada = 0
        # end if.

        listaPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(db).filter(idguia=int(objActividad.prueba_guia))

        total_ejercicios = len(listaPreguntas2BasicoMateriales)
        tipoEjercicio = listaPreguntas2BasicoMateriales[npregunta-1].tipo_ejercicio
        numeroCamposCompletar = listaPreguntas2BasicoMateriales[npregunta-1].num_campos_completar

        if tipoEjercicio == 1:  # ejercicio tipo fill
            maximo_intento = 3

        elif tipoEjercicio == 2:  # ejercicio de seleccion unica.

            if numeroCamposCompletar <= 4:
                maximo_intento = numeroCamposCompletar - 1
            else:
                maximo_intento = 3
            # end if.

        elif tipoEjercicio == 3:   # ejercicio de seleccion multiple.

            maximo_intento = 3
        else:
            maximo_intento = 3      # por defecto maximo 3 intentos.
        # end if.


        if (aprobada == 1) or (intento == maximo_intento):
            if npregunta == total_ejercicios:
                return redirect('portadaFinalRepaso')
            else:
                npregunta = npregunta + 1
                intento = 0
        # end if.

        posiciones = str(listaPreguntas2BasicoMateriales[npregunta-1].posiciones_botones)
        pos_boton = posiciones.replace('!', "")
        lista_pos = pos_boton.split(',')
        posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]
        img = base64.b64encode(listaPreguntas2BasicoMateriales[npregunta-1].imagen).decode()
        tipoEjercicio = listaPreguntas2BasicoMateriales[npregunta-1].tipo_ejercicio
        num_campos_completar = listaPreguntas2BasicoMateriales[npregunta-1].num_campos_completar

        alternativa = {1: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa1),
                       2: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa2),
                       3: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa3),
                       4: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa4),
                       5: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa5),
                       6: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa6),
                       7: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa7),
                       8: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa8)
                       }


        data = {
            'id_alumno_actividad': objUltimaActividadAlumno.id_alumno_actividad,
            'nombre_actividad': objActividad.nombre_actividad,
            'total_ejercicios': total_ejercicios,
            'npregunta': npregunta,
            'tipoEjercicio': tipoEjercicio,
            'num_campos_completar': num_campos_completar,
            'img': img,
            'botones': posicion_boton,
            'alternativa': alternativa
        }

    return render(request, 'visores/visorRepaso.html', data)

def guardaRespuestaVisorRepaso(request):

    response = {'estatus': 1, 'mensaje': ''}

    # fecha actual
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    # parametros enviados por POST.
    id_alumno_actividad = request.POST['id_alumno_actividad']
    npregunta = int(request.POST['npregunta'])
    tipo_ejercicio = int(request.POST['tipo_ejercicio'])
    num_campos_completar = int(request.POST['num_campos_completar'])
    respuestasAlumno = request.POST['respuestasAlumno']


    # nombre de la base de datos de la actividad.
    bd = 'materiales'

    objTblAlumnoActividades = TblAlumnoActividades.objects.filter(id_alumno_actividad=id_alumno_actividad)
    pruebaGuia = int(objTblAlumnoActividades[0].id_contenido_fase_actividad.id_actividad.prueba_guia)

    # consulta las respuestas del alumno.
    objTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objTblAlumnoActividades[0], npregunta=npregunta, prueba_guia=pruebaGuia)

    if objTblAlumnoRespuestasActividad:
        intento = int(objTblAlumnoRespuestasActividad.last().intento)+1
    else:
        intento = 1

    # consultar Tipo de ejercicio y cantidad de alternativas.
    objPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=pruebaGuia, npregunta=npregunta)

    if objPreguntas2BasicoMateriales[0].solucion_imagen is None:
        solucion_imagen = ''
    else:
        solucion_imagen = base64.b64encode(objPreguntas2BasicoMateriales[0].solucion_imagen).decode()

    # Consulta la Respuesta correcta
    objPreguntasInstanciasMateriales = PreguntasInstanciasMateriales.objects.using(bd).filter(idguia=pruebaGuia, npregunta=npregunta)

    respuesta_correcta = objPreguntasInstanciasMateriales[0].respuesta_pregunta


    if tipo_ejercicio == 1:  # ejercicio tipo fill

        maximo_intento = 3

        cantidadRespuestasCorrectas = 0
        listaRespuestasAlumno = respuestasAlumno.split(sep='~')
        listaRespuestaCorrecta = respuesta_correcta.split(sep='~')
        listaCondicionFill = []

        for x in range(num_campos_completar):
            if listaRespuestaCorrecta[x] == listaRespuestasAlumno[x]:
                cantidadRespuestasCorrectas += 1
                listaCondicionFill.append('correcto')
            else:
                listaCondicionFill.append('incorrecto')
        # end for.

        aprobada = cantidadRespuestasCorrectas / num_campos_completar


    elif tipo_ejercicio == 2:  # ejercicio de seleccion unica.

        if respuesta_correcta == respuestasAlumno:
            aprobada = 1
        else:
            aprobada = 0

        if num_campos_completar <= 4:
            maximo_intento = num_campos_completar - 1
        else:
            maximo_intento = 3
        # end if.


    elif tipo_ejercicio == 3:  # ejercicio de seleccion multiple.

        maximo_intento = 3

        listaRespuestas = respuesta_correcta.replace('~', ",").split(sep=',')

        if listaRespuestas[0] == respuestasAlumno:
            aprobada = 1
        else:
            aprobada = 0
    else:
        maximo_intento = 3
    # end if.

    # guarda la respuesta  del alumno.
    registroRespuesta = TblAlumnoRespuestasActividad(id_alumno_actividad=objTblAlumnoActividades[0], npregunta=npregunta, respuesta_alumno=respuestasAlumno, fecha=fechaActual, aprobada=aprobada, intento=intento, prueba_guia=pruebaGuia, nvuelta=1)

    try:
        registroRespuesta.save()
    except:
        response = {'estatus': 0, 'mensaje': 'error al guardar en la tabla tbl_alumno_respuestas_actividad'}

    response['aprobada'] = aprobada

    if aprobada == 1 or intento == maximo_intento:
        response['solucion_imagen'] = solucion_imagen
    # end if.

    if intento < maximo_intento:    # tiene mas intentos?
        response['TieneMasIntentos'] = 'SI'

        if tipo_ejercicio == 1:     # es un ejercicio tipo fill?.
            response['listaCondicionFill'] = listaCondicionFill
        # end if.

    else:
        response['TieneMasIntentos'] = 'NO'
        response['respuesta_correcta'] = respuesta_correcta
    # end if

    return HttpResponse(json.dumps(response))

def portadaFinalRepaso(request):

    # fecha actual
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    bd = 'materiales'

    # parametros de sesion.
    rutAlumno = request.session['rut']

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rutAlumno)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).exclude(id_contenido_fase_actividad__id_fase__id_fase=1).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        pruebaGuia = int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.prueba_guia)

        if objUltimaActividadAlumno.puntaje is None and objUltimaActividadAlumno.fecha_fin is None:

            # consultar total de preguntas de la actividad y tipo de pregunta
            listaPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=pruebaGuia)
            Totalpreguntas = 0
            tipoEjercicio = {}
            if listaPreguntas2BasicoMateriales:
                Totalpreguntas = len(listaPreguntas2BasicoMateriales)
                for objPreguntas2BasicoMateriales in listaPreguntas2BasicoMateriales:
                    tipoEjercicio[int(objPreguntas2BasicoMateriales.npregunta)] = int(objPreguntas2BasicoMateriales.tipo_ejercicio)
                # end for.
            # end if.

            intentosPregunta = {}
            puntajeParcialFill = {}
            puntajeFinalAlternativaUnica = {}
            puntajeFinalAlternativaMultiple = {}
            listaPreguntas = []
            listaTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objUltimaActividadAlumno, prueba_guia=pruebaGuia).order_by('npregunta', 'intento')

            if listaTblAlumnoRespuestasActividad:

                for objTblAlumnoRespuestasActividad in listaTblAlumnoRespuestasActividad:

                    if int(objTblAlumnoRespuestasActividad.npregunta) not in listaPreguntas:
                        listaPreguntas.append(int(objTblAlumnoRespuestasActividad.npregunta))

                    intentosPregunta[int(objTblAlumnoRespuestasActividad.npregunta)] = int(objTblAlumnoRespuestasActividad.intento)

                    if tipoEjercicio[int(objTblAlumnoRespuestasActividad.npregunta)] == 1:  # ejercicio tipo fill.

                        if int(objTblAlumnoRespuestasActividad.npregunta) not in puntajeParcialFill:
                            puntajeParcialFill[int(objTblAlumnoRespuestasActividad.npregunta)] = 0
                        # end if.
                        puntajeParcialFill[int(objTblAlumnoRespuestasActividad.npregunta)] += float(objTblAlumnoRespuestasActividad.aprobada)

                    elif tipoEjercicio[int(objTblAlumnoRespuestasActividad.npregunta)] == 2:  # ejercicio tipo seleccion unica.
                        puntajeFinalAlternativaUnica[int(objTblAlumnoRespuestasActividad.npregunta)] = int(objTblAlumnoRespuestasActividad.aprobada)

                    elif tipoEjercicio[int(objTblAlumnoRespuestasActividad.npregunta)] == 3:  # ejercicio tipo seleccion multiple.
                        puntajeFinalAlternativaMultiple[int(objTblAlumnoRespuestasActividad.npregunta)] = int(objTblAlumnoRespuestasActividad.aprobada)
                    # end if.
                # end for.

                puntajePreguntas = 0
                # finalmente volver a recorrer las preguntas para calculos finales.
                for npregunta in listaPreguntas:

                    if tipoEjercicio[npregunta] == 1:  # ejercicio tipo fill.
                        puntajePreguntas += (puntajeParcialFill[npregunta] / intentosPregunta[npregunta])

                    elif tipoEjercicio[npregunta] == 2:  # ejercicio tipo seleccion unica.
                        puntajePreguntas += (puntajeFinalAlternativaUnica[npregunta] / intentosPregunta[npregunta])

                    elif tipoEjercicio[npregunta] == 3:  # ejercicio tipo seleccion multiple.
                        puntajePreguntas += (puntajeFinalAlternativaMultiple[npregunta] / intentosPregunta[npregunta])
                    # end if.

                # end for.

                puntajeActividad = redondeo((puntajePreguntas / Totalpreguntas) * 100)

                # si el puntaje de la actividad es cero, se sustituye por 1.
                if puntajeActividad == 0:
                    puntajeActividad = 1
                # end if.

                objUltimaActividadAlumno.puntaje = puntajeActividad
                objUltimaActividadAlumno.fecha_fin = fechaActual
                try:
                    objUltimaActividadAlumno.save()
                except:
                    print('error al actualizar el puntaje de la actividad')

            # end if.

    data = {
        'nombre_actividad': objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad,
        'puntaje': objUltimaActividadAlumno.puntaje,
    }

    return render(request, 'visores/portadaFinalRepaso.html', data)

def portadaInicialEvaluacion(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('/ggalbas/index')

        # nombre de la base de datos donde se encuentra la actividad.
    db = 'e_test'

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).exclude(id_contenido_fase_actividad__id_fase__id_fase=1).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()

        if int(objUltimaActividadAlumno.intento) == 1:
            porcentaje_aprobacion = 65

        if int(objUltimaActividadAlumno.intento) == 2:
            porcentaje_aprobacion = 50

        if int(objUltimaActividadAlumno.intento) == 3:
            porcentaje_aprobacion = 50

        # consulta las respuestas del alumno.
        objTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objUltimaActividadAlumno)

        if objTblAlumnoRespuestasActividad:
            nvuelta = int(objTblAlumnoRespuestasActividad.last().nvuelta)
        else:
            nvuelta = 1
        # end if.

    # end if.
    data = {
        'porcentaje_aprobacion': porcentaje_aprobacion
    }

    return render(request, 'visores/portadaInicialEvaluacion.html', data)

def visorEvaluacion(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('/ggalbas/index')

    # nombre de la base de datos donde se encuentra la actividad.
    db = 'e_test'

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase=4).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()
        objActividadAlumno = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido_fase_actividad),diferenciado=int(objUltimaActividadAlumno.diferenciado)).order_by('-fecha_inicio')
        objActividad = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad
        intento_actividad = int(objActividadAlumno[0].intento)

        # si el campo prueba_guia esta vacio , busca la actividad en materiales  y actualiza los campos.
        if objActividad.prueba_guia is None:

            obPruebas = Pruebas.objects.using(db).filter(codprueba=objActividad.nombre_actividad)
            if obPruebas:
                objActividad.prueba_guia = int(obPruebas[0].idprueba)
                objActividad.descripcion_actividades = obPruebas[0].descprueba
                objActividad.npreguntas = int(obPruebas[0].npreguntas)
                try:
                    objActividad.save()
                except:
                    return HttpResponse('error al actualizar la tabla tbl_actividades')
            else:
                return HttpResponse('error, no existe la actividad en base de datos e_test.')
        # end if.

        # consulta las preguntas en e_test para conocer el tipo de ejercicio, numero de campos a completar.
        listaPreguntas2Basico = Preguntas2Basico.objects.using(db).filter(idprueba=int(objActividad.prueba_guia))

        # total de ejercicios.
        total_ejercicios = len(listaPreguntas2Basico)

        # consulta las respuestas del alumno.
        listaTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objUltimaActividadAlumno)

        if listaTblAlumnoRespuestasActividad:
            npregunta = int(listaTblAlumnoRespuestasActividad.last().npregunta)
            intento = int(listaTblAlumnoRespuestasActividad.last().intento)
            aprobada = float(listaTblAlumnoRespuestasActividad.last().aprobada)
            nvuelta = int(listaTblAlumnoRespuestasActividad.last().nvuelta)

            if nvuelta == 1:  # modo evaluacion.

                if npregunta == total_ejercicios:  # si llegue a la ultima pregunta de la primera vuelta.

                    # calculo de puntaje solo considerando ejercicios de la primera vuelta.
                    puntajePreguntas = 0
                    listaPreguntasSegundaVuelta = []

                    for objTblAlumnoRespuestasActividad in listaTblAlumnoRespuestasActividad:
                        if int(objTblAlumnoRespuestasActividad.nvuelta) == 1:
                            if float(objTblAlumnoRespuestasActividad.aprobada) < 1:
                                listaPreguntasSegundaVuelta.append(objTblAlumnoRespuestasActividad.npregunta)
                            puntajePreguntas += float(objTblAlumnoRespuestasActividad.aprobada)
                        # end if.

                    puntajeActividad = (puntajePreguntas / total_ejercicios) * 100

                    if puntajeActividad == 0:
                        puntajeActividad = 1

                    if intento_actividad == 1:

                        if puntajeActividad < 65:
                            return redirect('portadaFinalEvaluacion')

                        if 65 <= puntajeActividad < 100:
                            npregunta = listaPreguntasSegundaVuelta[0]  # primera pregunta de la segunda vuelta.
                            nvuelta = 2

                        if puntajeActividad == 100:
                            return redirect('portadaFinalEvaluacion')

                    if intento_actividad == 2:

                        if puntajeActividad < 50:
                            return redirect('portadaFinalEvaluacion')

                        if 50 <= puntajeActividad < 65:
                            npregunta = listaPreguntasSegundaVuelta[0]  # primera pregunta de la segunda vuelta.
                            nvuelta = 2

                        if 65 <= puntajeActividad < 100:
                            npregunta = listaPreguntasSegundaVuelta[0]  # primera pregunta de la segunda vuelta.
                            nvuelta = 2

                        if puntajeActividad == 100:
                            return redirect('portadaFinalEvaluacion')

                    if intento_actividad == 3:

                        if puntajeActividad < 50:
                            npregunta = listaPreguntasSegundaVuelta[0]  # primera pregunta de la segunda vuelta.
                            nvuelta = 2

                        if 50 <= puntajeActividad < 65:
                            npregunta = listaPreguntasSegundaVuelta[0]  # primera pregunta de la segunda vuelta.
                            nvuelta = 2

                        if 65 <= puntajeActividad < 100:
                            npregunta = listaPreguntasSegundaVuelta[0]  # primera pregunta de la segunda vuelta.
                            nvuelta = 2

                        if puntajeActividad == 100:
                            return redirect('portadaFinalEvaluacion')


                else:
                    npregunta = npregunta + 1
                # end if.

            elif nvuelta == 2:  # modo aprendizaje.

                tipoEjercicio = listaPreguntas2Basico[npregunta-1].tipo_ejercicio
                numeroCamposCompletar = int(listaPreguntas2Basico[npregunta-1].num_campos_completar)
                maximo_intento = 3

                if tipoEjercicio == 1:
                    maximo_intento = 3

                if tipoEjercicio == 2:

                    if numeroCamposCompletar <= 4:
                        maximo_intento = numeroCamposCompletar - 1
                    else:
                        maximo_intento = 3

                if tipoEjercicio == 3:
                    maximo_intento = 3


                if (aprobada == 1) or (intento == maximo_intento):

                    # buscar la lista de las preguntas de la segunda vuelta.
                    listaPreguntasSegundaVuelta = []
                    for objTblAlumnoRespuestasActividad in listaTblAlumnoRespuestasActividad:
                        if int(objTblAlumnoRespuestasActividad.nvuelta) == 1 and float(objTblAlumnoRespuestasActividad.aprobada) < 1:
                            listaPreguntasSegundaVuelta.append(objTblAlumnoRespuestasActividad.npregunta)
                        # end if.

                    if npregunta == listaPreguntasSegundaVuelta[-1]:  # si llegue a la ultima pregunta de la segunda vuelta.
                        return redirect('portadaFinalEvaluacion')

                    else:
                        indiceSiguientePregunta = listaPreguntasSegundaVuelta.index(npregunta) + 1  # busca la siguiente pregunta de la segunda vuelta.
                        npregunta = listaPreguntasSegundaVuelta[indiceSiguientePregunta]
                # end if.

        else:
            npregunta = 1
            nvuelta = 1
        # end if.


        # consulta los datos de la pregunta actual.

        # posiciones de las alternativas
        posiciones = str(listaPreguntas2Basico[npregunta - 1].posiciones_botones)
        pos_boton = posiciones.replace('!', "")
        lista_pos = pos_boton.split(',')
        posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]

        # imagen
        img = base64.b64encode(listaPreguntas2Basico[npregunta - 1].imagen).decode()

        # numero de campos a completar.
        num_campos_completar = listaPreguntas2Basico[npregunta - 1].num_campos_completar

        # tipo de ejercicio.
        tipoEjercicio = listaPreguntas2Basico[npregunta - 1].tipo_ejercicio

        maximo_intento = 3

        if tipoEjercicio == 1 or tipoEjercicio == 3:
            maximo_intento = 3

        if tipoEjercicio == 2:
            if num_campos_completar <= 4:
                maximo_intento = num_campos_completar - 1
            else:
                maximo_intento = 3

        # alternativas de respuestas.
        alternativa = {1: str(listaPreguntas2Basico[npregunta - 1].alternativa1),
                       2: str(listaPreguntas2Basico[npregunta - 1].alternativa2),
                       3: str(listaPreguntas2Basico[npregunta - 1].alternativa3),
                       4: str(listaPreguntas2Basico[npregunta - 1].alternativa4),
                       5: str(listaPreguntas2Basico[npregunta - 1].alternativa5),
                       6: str(listaPreguntas2Basico[npregunta - 1].alternativa6),
                       7: str(listaPreguntas2Basico[npregunta - 1].alternativa7),
                       8: str(listaPreguntas2Basico[npregunta - 1].alternativa8)
                       }

        data = {
            'id_alumno_actividad': objUltimaActividadAlumno.id_alumno_actividad,
            'nombre_actividad': objActividad.nombre_actividad,
            'intento_actividad': intento_actividad,
            'total_ejercicios': total_ejercicios,
            'npregunta': npregunta,
            'tipoEjercicio': tipoEjercicio,
            'num_campos_completar': num_campos_completar,
            'maximo_intento': maximo_intento,
            'nvuelta': nvuelta,
            'img': img,
            'botones': posicion_boton,
            'alternativa': alternativa
        }

    return render(request, 'visores/visorEvaluacion.html', data)

def guardaRespuestaVisorEvaluacion(request):

    response = {'estatus': 1, 'mensaje': ''}

    # fecha actual
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    # parametros enviados por POST.
    id_alumno_actividad = request.POST['id_alumno_actividad']
    npregunta = int(request.POST['npregunta'])
    tipo_ejercicio = int(request.POST['tipo_ejercicio'])
    num_campos_completar = int(request.POST['num_campos_completar'])
    respuestaAlumno = request.POST['respuestaAlumno']
    nvuelta = int(request.POST['nvuelta'])
    maximo_intento = int(request.POST['maximo_intento'])
    total_ejercicios = int(request.POST['total_ejercicios'])

    # nombre de la base de datos de la actividad.
    bd = 'e_test'

    objTblAlumnoActividades = TblAlumnoActividades.objects.filter(id_alumno_actividad=id_alumno_actividad)

    pruebaGuia = int(objTblAlumnoActividades[0].id_contenido_fase_actividad.id_actividad.prueba_guia)

    # consulta las respuestas del alumno.
    objTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objTblAlumnoActividades[0], npregunta=npregunta, nvuelta=nvuelta, prueba_guia=pruebaGuia)

    if objTblAlumnoRespuestasActividad:
        intento = int(objTblAlumnoRespuestasActividad.last().intento)+1
    else:
        intento = 1

    # Consulta la Respuesta correcta
    objPreguntasInstancias = PreguntasInstancias.objects.using(bd).filter(idprueba=pruebaGuia, npregunta=npregunta)
    respuesta_correcta = objPreguntasInstancias[0].respuesta_pregunta

    aprobada = 0
    listaCondicionFill = []

    if tipo_ejercicio == 1:  # ejercicio tipo fill

        cantidadRespuestasCorrectas = 0
        listaRespuestasAlumno = respuestaAlumno.split(sep='~')
        listaRespuestaCorrecta = respuesta_correcta.split(sep='~')

        for x in range(num_campos_completar):
            if listaRespuestaCorrecta[x] == listaRespuestasAlumno[x]:
                cantidadRespuestasCorrectas += 1
                listaCondicionFill.append('correcto')
            else:
                listaCondicionFill.append('incorrecto')
        # end for.

        aprobada = cantidadRespuestasCorrectas / num_campos_completar

    if tipo_ejercicio == 2:  # ejercicio de seleccion unica.

        if respuesta_correcta == respuestaAlumno:
            aprobada = 1
        else:
            aprobada = 0

    if tipo_ejercicio == 3:  # ejercicio de seleccion multiple.

        listaRespuestas = respuesta_correcta.replace('~', ",").split(sep=',')

        if listaRespuestas[0] == respuestaAlumno:
            aprobada = 1
        else:
            aprobada = 0

    # end if.

    # guarda la respuesta  del alumno.
    registroRespuesta = TblAlumnoRespuestasActividad(id_alumno_actividad=objTblAlumnoActividades[0], npregunta=npregunta, respuesta_alumno=respuestaAlumno, fecha=fechaActual, aprobada=aprobada, intento=intento, nvuelta=nvuelta, prueba_guia=pruebaGuia)

    try:
        registroRespuesta.save()
    except:
        response = {'estatus': 0, 'mensaje': 'error al guardar en la tabla tbl_alumno_respuestas_actividad'}

    if nvuelta == 1:

        if total_ejercicios == npregunta:  # si guardo la ultima pregunta de la primera vuelta, obtengo el puntaje total de la actividad

            puntajePreguntas = 0

            listaTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objTblAlumnoActividades[0], nvuelta=nvuelta, prueba_guia=pruebaGuia)

            for objTblAlumnoRespuestasActividad in listaTblAlumnoRespuestasActividad:
                puntajePreguntas += float(objTblAlumnoRespuestasActividad.aprobada)

            puntajeActividad = (puntajePreguntas / total_ejercicios) * 100

            if puntajeActividad == 0:
                puntajeActividad = 1

            response['puntajeActividad'] = puntajeActividad


    if nvuelta == 2:

        response['aprobada'] = aprobada

        response['intento'] = intento

        if aprobada == 1 or intento == maximo_intento:

            # consultar la imagen solucion del ejercicio.
            objPreguntas2Basico = Preguntas2Basico.objects.using(bd).filter(idprueba=pruebaGuia, npregunta=npregunta)

            if objPreguntas2Basico[0].solucion_imagen is None:
                response['solucion_imagen'] = ''
            else:
                response['solucion_imagen'] = base64.b64encode(objPreguntas2Basico[0].solucion_imagen).decode()

        if intento == maximo_intento:
            response['respuesta_correcta'] = respuesta_correcta

        if intento < maximo_intento and tipo_ejercicio == 1:  # es un ejercicio tipo fill?.
            response['listaCondicionFill'] = listaCondicionFill


    return HttpResponse(json.dumps(response))

def portadaIntermediaEvaluacion(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('/ggalbas/index')

        # nombre de la base de datos donde se encuentra la actividad.
    db = 'e_test'

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase=4).order_by('fecha_inicio')

    if listaObjAlumnoActividades:

        objUltimaActividadAlumno = listaObjAlumnoActividades.last()

        # consulta las preguntas en e_test para conocer el tipo de ejercicio, numero de campos a completar.
        listaPreguntas2Basico = Preguntas2Basico.objects.using(db).filter(idprueba=int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.prueba_guia))

        # total de ejercicios.
        total_ejercicios = len(listaPreguntas2Basico)

        # consulta las respuestas del alumno.
        listaTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objUltimaActividadAlumno)

        if listaTblAlumnoRespuestasActividad:

            # calculo de puntaje solo considerando ejercicios de la primera vuelta.
            puntajePreguntas = 0
            texto_portada = ''

            for objTblAlumnoRespuestasActividad in listaTblAlumnoRespuestasActividad:
                if int(objTblAlumnoRespuestasActividad.nvuelta) == 1:
                    puntajePreguntas += float(objTblAlumnoRespuestasActividad.aprobada)
                # end if.

            puntajeActividad = (puntajePreguntas / total_ejercicios) * 100

            # si el puntaje de la actividad es cero, se sustituye por 1.
            if puntajeActividad == 0:
                puntajeActividad = 1

            if 65 <= puntajeActividad < 100:
                texto_portada = 'procentaje_65_100'

            if 50 <= puntajeActividad < 65:
                texto_portada = 'procentaje_50_65'

            if puntajeActividad < 50:
                texto_portada = 'procentaje_50'

    data = {
        'texto_portada': texto_portada,
    }

    # end if.
    return render(request, 'visores/portadaIntermediaEvaluacion.html',data)

def portadaFinalEvaluacion(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('/ggalbas/index')

    # nombre de la base de datos donde se encuentra la actividad.
    db = 'e_test'

    # fecha actual
    now = datetime.datetime.now()
    fechaActual = now.strftime("%Y-%m-%d %H:%M:%S")

    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    ultimoContenido = 0

    if objAlumno[0].autonomo == 0:
        listaObjContenidoUnidad = TblContenidoUnidad.objects.filter(codigo_lista=objAlumno[0].codigo_lista).order_by('id_unidad__orden', 'orden')
        ObjUltimoContenidoUnidad = listaObjContenidoUnidad.last()

        if objAlumno[0].id_producto.id_producto == 3:
            contenidoDiferenciado=TblContenidos.objects.filter(id_padre=int(ObjUltimoContenidoUnidad.id_contenido.id_contenido))
            ultimoContenido=int(contenidoDiferenciado[0].id_contenido)
        else:
            ultimoContenido = int(ObjUltimoContenidoUnidad.id_contenido.id_contenido)

    if objAlumno[0].autonomo == 1:
        listaTblPlanAutonomo = TblPlanAutonomo.objects.filter(rut_alumno=objAlumno[0]).order_by('id_unidad__orden', 'orden')
        objUltimoPlanAutonomo = listaTblPlanAutonomo.last()
        ultimoContenido = int(objUltimoPlanAutonomo.id_contenido.id_contenido)

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0], id_contenido_fase_actividad__id_fase__id_fase=4).order_by('fecha_inicio')

    objUltimaActividadAlumno = listaObjAlumnoActividades.last()
    intentoActividad = int(objUltimaActividadAlumno.intento)
    pruebaGuia = int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.prueba_guia)
    nombreActividad = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad

    if objUltimaActividadAlumno.fecha_fin is None and objUltimaActividadAlumno.puntaje is None:

        # consulta las preguntas en e_test para conocer el tipo de ejercicio, numero de campos a completar.
        listaPreguntas2Basico = Preguntas2Basico.objects.using(db).filter(idprueba=pruebaGuia)

        # total de ejercicios.
        total_ejercicios = len(listaPreguntas2Basico)

        # consulta las respuestas del alumno.
        listaTblAlumnoRespuestasActividad = TblAlumnoRespuestasActividad.objects.filter(id_alumno_actividad=objUltimaActividadAlumno, prueba_guia=pruebaGuia)

        if listaTblAlumnoRespuestasActividad:

            # calculo de puntaje solo considerando ejercicios de la primera vuelta.
            puntajePreguntas = 0

            for objTblAlumnoRespuestasActividad in listaTblAlumnoRespuestasActividad:
                if int(objTblAlumnoRespuestasActividad.nvuelta) == 1:
                    puntajePreguntas += float(objTblAlumnoRespuestasActividad.aprobada)
                # end if.

            puntajeActividad = (puntajePreguntas / total_ejercicios) * 100

            if puntajeActividad == 0:
                puntajeActividad = 1

            objUltimaActividadAlumno.puntaje = redondeo(puntajeActividad)
            objUltimaActividadAlumno.fecha_fin = fechaActual
            try:
                objUltimaActividadAlumno.save()
            except:
                print('error al actualizar el puntaje de la actividad.')

            listaObjPlan = TblPlan.objects.filter(rut_alumno=objAlumno[0]).order_by('fecha_inicio')

            if listaObjPlan:

                objplanActual = listaObjPlan.last()
                objplanActual.fecha_fin = objUltimaActividadAlumno.fecha_fin

                try:
                    objplanActual.save()
                except:
                    print('error al actualizar en la tabla tbl_plan.')

            if ultimoContenido == int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_contenido.id_contenido):

                if intentoActividad == 1 and puntajeActividad >= 65:

                    try:
                        objAlumno.update(libre=1)
                    except:
                        print('error al actualizar')

                if intentoActividad == 2 and puntajeActividad >= 50:

                    try:
                        objAlumno.update(libre=1)
                    except:
                        print('error al actualizar')

                if intentoActividad == 3:

                    try:
                        objAlumno.update(libre=1)
                    except:
                        print('error al actualizar')

    if intentoActividad == 1 and int(objUltimaActividadAlumno.puntaje) >= 65:
        url_boton = 'unidadesAlumno'
    elif intentoActividad == 2 and int(objUltimaActividadAlumno.puntaje) >= 50:
        url_boton = 'unidadesAlumno'
    elif intentoActividad == 3:
        url_boton = 'unidadesAlumno'
    else:
        url_boton = 'contenidosAlumno'



    data = {
        'nombre_actividad': nombreActividad,
        'puntaje': objUltimaActividadAlumno.puntaje,
        'url_boton': url_boton
    }

    return render(request, 'visores/portadaFinalEvaluacion.html', data)

def visorIntegracion(request):

    if request.session.get("rut", False):
        rut_alumno = request.session['rut']
    else:
        return redirect('/ggalbas/index')

    pais = flagPais(request)
    subdominio = obtenerSubdominio(request)

    if pais == 'cl' and subdominio == 'guiado':
        var_server_destino = 'minlocal.e-mat.cl'

    elif pais == 'cl' and subdominio == 'guiado2':
        var_server_destino = 'minlocal2.e-mat.cl'

    elif pais == 'cl' and subdominio == 'guiadodes':
        var_server_destino = 'minlocaldes.e-mat.cl'

    # caso Peru.
    elif pais == 'pe' and subdominio == 'guiado':
        var_server_destino = 'minlocal.e-mat.pe'

    else:
        var_server_destino = 'minlocaldes.e-mat.cl'


    objAlumno = TblAlumnos.objects.filter(rut_alumno=rut_alumno)

    libre = int(objAlumno[0].libre)

    listaA4GuiaInteligente = ['EXA4', 'EYA4', 'N8A4', 'CXA4', 'CYA4', 'GDA4', 'N9A4', 'CVA4', 'QAA4', 'QBA4', 'KAA4', 'KBA4', 'KCA4', 'HAA4', 'HBA4', 'HCA4', 'HEA4', 'HDA4', 'JAA4', 'JBA4', 'QCA4', 'QDA4', 'KDA4', 'KEA4', 'KFA4', 'KGA4', 'HFA4', 'HGA4', 'JCA4', 'JDA4', 'JEA4']

    # consultar la ultima actividad del alumno.
    listaObjAlumnoActividades = TblAlumnoActividades.objects.filter(rut_alumno=objAlumno[0]).exclude(id_contenido_fase_actividad__id_fase__id_fase=1).order_by('fecha_inicio')

    objUltimaActividadAlumno = listaObjAlumnoActividades.last()
    ultimasSiglasActividad = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad.strip()[-2:]
    nombre_actividad = objUltimaActividadAlumno.id_contenido_fase_actividad.id_actividad.nombre_actividad.strip()
    id_fase = int(objUltimaActividadAlumno.id_contenido_fase_actividad.id_fase.id_fase)

    tipo_visor = 0

    if ultimasSiglasActividad == 'A4' and nombre_actividad not in listaA4GuiaInteligente:
        tipo_visor = 1

    if ultimasSiglasActividad == 'Z1' or ultimasSiglasActividad == 'Z2' or ultimasSiglasActividad == 'Z4' or ultimasSiglasActividad == 'Z5' or ultimasSiglasActividad == 'Z6' or ultimasSiglasActividad == 'Z8' or ultimasSiglasActividad == 'Z0' or ultimasSiglasActividad == 'Z7' or ultimasSiglasActividad == 'Z9':
        tipo_visor = 2

    if ultimasSiglasActividad == 'A4' and nombre_actividad in listaA4GuiaInteligente:
        tipo_visor = 3

    url_boton_volver = ''

    if libre == 0 and id_fase == 3 or id_fase == 4:
        url_boton_volver = 'contenidosAlumno'

    if libre == 0 and id_fase == 5 or id_fase == 6 or id_fase == 7:
        url_boton_volver = 'complementariasUnidad'

    if libre == 1 and id_fase == 5 or id_fase == 6 or id_fase == 7:
        url_boton_volver = 'complementariasLibre'

    data = {
        'Rut': rut_alumno,
        'Alumno': objAlumno[0].nombre+', ' + objAlumno[0].apellido,
        'url_boton_volver': url_boton_volver,
        'nombre_actividad': nombre_actividad,
        'id_alumno_actividad': objUltimaActividadAlumno.id_alumno_actividad,
        'tipo_visor': tipo_visor,
        'Dominio': var_server_destino,
    }

    return render(request, 'visores/visorIntegracion.html', data)

def portadaInicialMeta(request):
    return render(request, 'visores/portadaInicialMeta.html')

def portadaFinalMeta(request):
    data = {}
    return render(request, 'visores/portadaFinalMeta.html', data)

def redondeo(x):
    return int(x + math.copysign(0.5, x))

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)