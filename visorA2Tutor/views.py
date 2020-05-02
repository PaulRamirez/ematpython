import json
import base64
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout

from core.models import Guias, Preguntas2BasicoMateriales, PreguntasInstanciasMateriales
from core.views import redondeo
from ggalbas.models import TblTutores


def portadaInicialModoAlumno(request, rut, modulo):

    data = {}
    db = 'materiales'

    objGuias = Guias.objects.using(db).filter(codguia=modulo.upper())

    if objGuias:
        data['descguia'] = objGuias[0].descguia
        data['codguia'] = objGuias[0].codguia

        objTblTutores = TblTutores.objects.filter(rut_tutor=rut)
        if objTblTutores:
            # si inicia o vuelve a repetir la actividad, entonces borro todas sus respuestas.
            request.session["listaRespuestasAlumno"] = {}
            request.session['npregunta'] = 1
            request.session['mostrarPantallaEjercicio'] = True
            request.session['terminoActividad'] = False
            request.session['rut_tutor'] = rut
            request.session['modulo'] = modulo.upper()
        else:
            return HttpResponse('El rut del tutor no se encontro.')
    else:
        return HttpResponse('El nombre del modulo no se encontro.')

    return render(request, 'visorA2Tutor/portadaInicialModoAlumno.html', data)

def portadaInicialModoTutor(request, rut, modulo):

    data = {}
    db = 'materiales'

    objGuias = Guias.objects.using(db).filter(codguia=modulo.upper())

    if objGuias:
        data['descguia'] = objGuias[0].descguia
        data['codguia'] = objGuias[0].codguia

        objTblTutores = TblTutores.objects.filter(rut_tutor=rut)
        if objTblTutores:
            # si inicia o vuelve a repetir la actividad, entonces borro todas sus respuestas.
            request.session["listaRespuestasAlumno"] = {}
            request.session['npregunta'] = 1
            request.session['mostrarPantallaEjercicio'] = True
            request.session['terminoActividad'] = False
            request.session['rut_tutor'] = rut
            request.session['modulo'] = modulo.upper()
        else:
            return HttpResponse('El rut del tutor no se encontro.')
    else:
        return HttpResponse('El nombre del modulo no se encontro.')

    return render(request, 'visorA2Tutor/portadaInicialModoTutor.html', data)

def visorModoAlumno(request):

    if "rut_tutor" not in request.session:
        return HttpResponse('la sesion ha caducado.')

    db = 'materiales'

    # recupera variables de sesion.
    modulo = request.session['modulo']
    npregunta = request.session['npregunta']
    mostrarPantallaEjercicio = request.session['mostrarPantallaEjercicio']
    terminoAct = request.session['terminoActividad']

    if terminoAct is True:
        return redirect('portadaFinalModoAlumno')

    # consulto los datos de la proxima pregunta a mostrar
    objGuias = Guias.objects.using(db).filter(codguia=modulo)
    listaPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(db).filter(idguia=int(objGuias[0].idguia))
    total_ejercicios = len(listaPreguntas2BasicoMateriales)
    posiciones = str(listaPreguntas2BasicoMateriales[npregunta-1].posiciones_botones)
    pos_boton = posiciones.replace('!', "")
    lista_pos = pos_boton.split(',')
    posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]
    img = base64.b64encode(listaPreguntas2BasicoMateriales[npregunta-1].imagen).decode()
    tipoEjercicio = listaPreguntas2BasicoMateriales[npregunta-1].tipo_ejercicio
    num_campos_completar = listaPreguntas2BasicoMateriales[npregunta-1].num_campos_completar
    maximo_intento = 3

    if tipoEjercicio == 1:  # ejercicio tipo fill
        maximo_intento = 3

    if tipoEjercicio == 2 and num_campos_completar <= 3:  # ejercicio de seleccion unica.
        maximo_intento = num_campos_completar - 1

    if tipoEjercicio == 2 and num_campos_completar >= 4:  # ejercicio de seleccion unica.
        maximo_intento = 3

    if tipoEjercicio == 3:   # ejercicio de seleccion multiple.
        maximo_intento = 3

    alternativa = {1: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa1),
                   2: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa2),
                   3: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa3),
                   4: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa4),
                   5: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa5),
                   6: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa6),
                   7: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa7),
                   8: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa8)
                   }

    if mostrarPantallaEjercicio:
        # if debo mostrar la pantalla del ejercicio
        img_solucion = ''
    else:
        # sino, debo mostrar la pantalla del pop
        img_solucion = base64.b64encode(listaPreguntas2BasicoMateriales[npregunta - 1].solucion_imagen).decode()


    data = {
        'idguia': int(objGuias[0].idguia),
        'nombre_actividad': objGuias[0].codguia,
        'total_ejercicios': total_ejercicios,
        'npregunta': npregunta,
        'tipoEjercicio': tipoEjercicio,
        'num_campos_completar': num_campos_completar,
        'maximo_intento': maximo_intento,
        'img': img,
        'botones': posicion_boton,
        'alternativa': alternativa,
        'mostrarPantallaEjercicio': mostrarPantallaEjercicio,
        'img_solucion': img_solucion
    }

    return render(request, 'visorA2Tutor/visorModoAlumno.html', data)

def visorModoTutor(request):

    if "rut_tutor" not in request.session:
        return HttpResponse('la sesion ha caducado.')

    db = 'materiales'

    # recupera variables de sesion.
    modulo = request.session['modulo']
    npregunta = request.session['npregunta']
    mostrarPantallaEjercicio = request.session['mostrarPantallaEjercicio']
    terminoAct = request.session['terminoActividad']

    if terminoAct is True:
        return redirect('portadaFinalModoTutor')

    # consulto los datos de la proxima pregunta a mostrar
    objGuias = Guias.objects.using(db).filter(codguia=modulo)
    listaPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(db).filter(idguia=int(objGuias[0].idguia))
    total_ejercicios = len(listaPreguntas2BasicoMateriales)
    posiciones = str(listaPreguntas2BasicoMateriales[npregunta-1].posiciones_botones)
    pos_boton = posiciones.replace('!', "")
    lista_pos = pos_boton.split(',')
    posicion_boton = [lista_pos[i:i + 4] for i in range(0, len(lista_pos), 4)]
    img = base64.b64encode(listaPreguntas2BasicoMateriales[npregunta-1].imagen).decode()
    tipoEjercicio = listaPreguntas2BasicoMateriales[npregunta-1].tipo_ejercicio
    num_campos_completar = listaPreguntas2BasicoMateriales[npregunta-1].num_campos_completar
    maximo_intento = 3

    if tipoEjercicio == 1:  # ejercicio tipo fill
        maximo_intento = 3

    if tipoEjercicio == 2 and num_campos_completar <= 3:  # ejercicio de seleccion unica.
        maximo_intento = num_campos_completar - 1

    if tipoEjercicio == 2 and num_campos_completar >= 4:  # ejercicio de seleccion unica.
        maximo_intento = 3

    if tipoEjercicio == 3:   # ejercicio de seleccion multiple.
        maximo_intento = 3

    alternativa = {1: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa1),
                   2: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa2),
                   3: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa3),
                   4: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa4),
                   5: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa5),
                   6: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa6),
                   7: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa7),
                   8: str(listaPreguntas2BasicoMateriales[npregunta-1].alternativa8)
                   }

    if mostrarPantallaEjercicio:
        # if debo mostrar la pantalla del ejercicio
        img_solucion = ''
    else:
        # sino, debo mostrar la pantalla del pop
        img_solucion = base64.b64encode(listaPreguntas2BasicoMateriales[npregunta - 1].solucion_imagen).decode()


    data = {
        'idguia': int(objGuias[0].idguia),
        'nombre_actividad': objGuias[0].codguia,
        'total_ejercicios': total_ejercicios,
        'npregunta': npregunta,
        'tipoEjercicio': tipoEjercicio,
        'num_campos_completar': num_campos_completar,
        'maximo_intento': maximo_intento,
        'img': img,
        'botones': posicion_boton,
        'alternativa': alternativa,
        'mostrarPantallaEjercicio': mostrarPantallaEjercicio,
        'img_solucion': img_solucion
    }

    return render(request, 'visorA2Tutor/visorModoTutor.html', data)

def guardaRespuestaModoAlumno(request):

    response = {'estatus': 1, 'mensaje': ''}

    idguia = int(request.POST['idguia'])
    npregunta = request.POST['npregunta']
    tipo_ejercicio = int(request.POST['tipo_ejercicio'])
    num_campos_completar = int(request.POST['num_campos_completar'])
    respuestaAlumno = request.POST['respuestaAlumno']
    maximo_intento = int(request.POST['maximo_intento'])
    total_ejercicios = int(request.POST['total_ejercicios'])

    # nombre de la base de datos de la actividad.
    bd = 'materiales'
    aprobada = 0
    listaCondicionFill = []

    # Consulta la Respuesta correcta
    objPreguntasInstancias = PreguntasInstanciasMateriales.objects.using(bd).filter(idguia=idguia, npregunta=int(npregunta))
    respuesta_pregunta = objPreguntasInstancias[0].respuesta_pregunta

    # Determinar si respondio correcto o incorrecto la pregunta.
    if tipo_ejercicio == 1:  # ejercicio tipo fill

        cantidadRespuestasCorrectas = 0
        listaRespuestasAlumno = respuestaAlumno.split(sep='~')
        listaRespuestaCorrecta = respuesta_pregunta.split(sep='~')

        for x in range(num_campos_completar):

            if listaRespuestaCorrecta[x] == listaRespuestasAlumno[x]:
                cantidadRespuestasCorrectas += 1
                listaCondicionFill.append('correcto')
            else:
                listaCondicionFill.append('incorrecto')


        aprobada = cantidadRespuestasCorrectas / num_campos_completar

    if tipo_ejercicio == 2:  # ejercicio de seleccion unica.

        if respuesta_pregunta == respuestaAlumno:
            aprobada = 1
        else:
            aprobada = 0

    if tipo_ejercicio == 3:  # ejercicio de seleccion multiple.

        listaRespuestas = respuesta_pregunta.split(sep='~')
        respuesta_correcta = listaRespuestas[0]

        if respuesta_correcta == respuestaAlumno:
            aprobada = 1
        else:
            aprobada = 0

    response['aprobada'] = aprobada


    if str(npregunta) in request.session['listaRespuestasAlumno']:
        ultimoIntento = len(request.session['listaRespuestasAlumno'][str(npregunta)])
        intento = ultimoIntento + 1
    else:
        intento = 1
        request.session['listaRespuestasAlumno'][str(npregunta)] = {}

    response['intento'] = intento

    # guardo el nuevo intento de la pregunta y tambien guardo en la sesion.
    request.session['listaRespuestasAlumno'][str(npregunta)][str(intento)] = aprobada

    # consultar la imagen solucion del ejercicio.
    objPreguntas2Basico = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=idguia, npregunta=int(npregunta))
    solucion_imagen = objPreguntas2Basico[0].solucion_imagen

    # si respondio incorrecto y aun tiene intento(s) y es un ejercicio tipo fill , le marco en rojo los casilleros donde se equivoco y en verde donde respondio correcto.
    if aprobada < 1 and intento < maximo_intento and tipo_ejercicio == 1:
        response['listaCondicionFill'] = listaCondicionFill

    # si respondio incorrecto y no tiene mas intentos, entonces le muestro la respuesta correcta.
    if aprobada < 1 and intento == maximo_intento:
        response['respuesta_pregunta'] = respuesta_pregunta

    # si contesto correcto o no tiene mas intentos y aun no llega a la ultima pregunta y no tiene pop  entonces avanzo a la siguiente pregunta
    if (aprobada == 1 or intento == maximo_intento) and int(npregunta) < total_ejercicios and solucion_imagen is None:

        # avanza a la siguiente pregunta
        siguientePregunta = int(npregunta) + 1
        request.session['npregunta'] = siguientePregunta

        # mostrar pagina de ejercicio
        request.session['mostrarPantallaEjercicio'] = True

        if str(siguientePregunta) in request.session['listaRespuestasAlumno']:
            del request.session['listaRespuestasAlumno'][str(siguientePregunta)]

    # si contesto correcto o no tiene mas intentos y aun no llega a la ultima pregunta y tiene pop  entonces muestro pop de la pregunta actual
    if (aprobada == 1 or intento == maximo_intento) and int(npregunta) < total_ejercicios and solucion_imagen is not None:
        request.session['mostrarPantallaEjercicio'] = False

    if (aprobada == 1 or intento == maximo_intento) and int(npregunta) == total_ejercicios and solucion_imagen is not None:
        request.session['mostrarPantallaEjercicio'] = False

    response['npregunta'] = request.session['npregunta']
    response['mostrarPantallaEjercicio'] = request.session['mostrarPantallaEjercicio']

    return HttpResponse(json.dumps(response))

def guardaRespuestaModoTutor(request):

    response = {'estatus': 1, 'mensaje': ''}

    idguia = int(request.POST['idguia'])
    npregunta = request.POST['npregunta']
    tipo_ejercicio = int(request.POST['tipo_ejercicio'])
    num_campos_completar = int(request.POST['num_campos_completar'])
    respuestaAlumno = request.POST['respuestaAlumno']
    maximo_intento = int(request.POST['maximo_intento'])
    total_ejercicios = int(request.POST['total_ejercicios'])

    # nombre de la base de datos de la actividad.
    bd = 'materiales'
    aprobada = 0
    listaCondicionFill = []

    # Consulta la Respuesta correcta
    objPreguntasInstancias = PreguntasInstanciasMateriales.objects.using(bd).filter(idguia=idguia, npregunta=int(npregunta))
    respuesta_pregunta = objPreguntasInstancias[0].respuesta_pregunta

    # Determinar si respondio correcto o incorrecto la pregunta.
    if tipo_ejercicio == 1:  # ejercicio tipo fill

        cantidadRespuestasCorrectas = 0
        listaRespuestasAlumno = respuestaAlumno.split(sep='~')
        listaRespuestaCorrecta = respuesta_pregunta.split(sep='~')

        for x in range(num_campos_completar):

            if listaRespuestaCorrecta[x] == listaRespuestasAlumno[x]:
                cantidadRespuestasCorrectas += 1
                listaCondicionFill.append('correcto')
            else:
                listaCondicionFill.append('incorrecto')


        aprobada = cantidadRespuestasCorrectas / num_campos_completar

    if tipo_ejercicio == 2:  # ejercicio de seleccion unica.

        if respuesta_pregunta == respuestaAlumno:
            aprobada = 1
        else:
            aprobada = 0

    if tipo_ejercicio == 3:  # ejercicio de seleccion multiple.

        listaRespuestas = respuesta_pregunta.split(sep='~')
        respuesta_correcta = listaRespuestas[0]

        if respuesta_correcta == respuestaAlumno:
            aprobada = 1
        else:
            aprobada = 0

    response['aprobada'] = aprobada


    if str(npregunta) in request.session['listaRespuestasAlumno']:
        ultimoIntento = len(request.session['listaRespuestasAlumno'][str(npregunta)])
        intento = ultimoIntento + 1
    else:
        intento = 1
        request.session['listaRespuestasAlumno'][str(npregunta)] = {}

    response['intento'] = intento

    # guardo el nuevo intento de la pregunta y tambien guardo en la sesion.
    request.session['listaRespuestasAlumno'][str(npregunta)][str(intento)] = aprobada

    # consultar la imagen solucion del ejercicio.
    objPreguntas2Basico = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=idguia, npregunta=int(npregunta))
    solucion_imagen = objPreguntas2Basico[0].solucion_imagen

    # si respondio incorrecto y aun tiene intento(s) y es un ejercicio tipo fill , le marco en rojo los casilleros donde se equivoco y en verde donde respondio correcto.
    if aprobada < 1 and intento < maximo_intento and tipo_ejercicio == 1:
        response['listaCondicionFill'] = listaCondicionFill

    # si respondio incorrecto y no tiene mas intentos, entonces le muestro la respuesta correcta.
    if aprobada < 1 and intento == maximo_intento:
        response['respuesta_pregunta'] = respuesta_pregunta

    # si contesto correcto o no tiene mas intentos y aun no llega a la ultima pregunta y no tiene pop  entonces avanzo a la siguiente pregunta
    if (aprobada == 1 or intento == maximo_intento) and int(npregunta) < total_ejercicios and solucion_imagen is None:

        # avanza a la siguiente pregunta
        siguientePregunta = int(npregunta) + 1
        request.session['npregunta'] = siguientePregunta

        # mostrar pagina de ejercicio
        request.session['mostrarPantallaEjercicio'] = True

        if str(siguientePregunta) in request.session['listaRespuestasAlumno']:
            del request.session['listaRespuestasAlumno'][str(siguientePregunta)]

    # si contesto correcto o no tiene mas intentos y aun no llega a la ultima pregunta y tiene pop  entonces muestro pop de la pregunta actual
    if (aprobada == 1 or intento == maximo_intento) and int(npregunta) < total_ejercicios and solucion_imagen is not None:
        request.session['mostrarPantallaEjercicio'] = False

    if (aprobada == 1 or intento == maximo_intento) and int(npregunta) == total_ejercicios and solucion_imagen is not None:
        request.session['mostrarPantallaEjercicio'] = False

    response['npregunta'] = request.session['npregunta']
    response['mostrarPantallaEjercicio'] = request.session['mostrarPantallaEjercicio']

    return HttpResponse(json.dumps(response))

def irPantallaEjercicio(request):

    response = {'estatus': 1, 'mensaje': ''}

    npregunta = int(request.POST['npregunta'])

    # posicionar en la nueva pregunta
    request.session['npregunta'] = npregunta

    # limpiar pregunta.
    if str(npregunta) in request.session['listaRespuestasAlumno']:
        del request.session['listaRespuestasAlumno'][str(npregunta)]

    # activar pantalla del ejercicio.
    request.session['mostrarPantallaEjercicio'] = True

    return HttpResponse(json.dumps(response))

def irPantallaPop(request):

    response = {'estatus': 1, 'mensaje': ''}

    npregunta = int(request.POST['npregunta'])

    # posicionar en la nueva pregunta
    request.session['npregunta'] = npregunta

    # activar pantalla del pop.
    request.session['mostrarPantallaEjercicio'] = False

    return HttpResponse(json.dumps(response))

def terminoActividad(request):

    response = {'estatus': 1, 'mensaje': ''}

    # finalizar actividad
    request.session['terminoActividad'] = True

    return HttpResponse(json.dumps(response))

def buscarImagenSolucionEjercicio(request):

    response = {'estatus': 1, 'mensaje': ''}
    bd = 'materiales'
    modulo = request.session['modulo']
    objGuias = Guias.objects.using(bd).filter(codguia=modulo)
    npregunta = int(request.POST['npregunta'])

    objPreguntas2Basico = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=objGuias[0].idguia, npregunta=int(npregunta))

    if objPreguntas2Basico[0].solucion_imagen is None:
        response['solucion_imagen'] = ''
    else:
        response['solucion_imagen'] = base64.b64encode(objPreguntas2Basico[0].solucion_imagen).decode()

    return HttpResponse(json.dumps(response))

def portadaFinalModoAlumno(request):

    if "rut_tutor" not in request.session:
        return HttpResponse('la sesion ha caducado.')

    bd = 'materiales'
    modulo = request.session['modulo']
    objGuias = Guias.objects.using(bd).filter(codguia=modulo)
    puntajePreguntas = 0

    # consultar total de preguntas de la actividad y tipo de pregunta
    listaPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=int(objGuias[0].idguia))
    Totalpreguntas = len(listaPreguntas2BasicoMateriales)
    tipoEjercicio = {}

    for objPreguntas2BasicoMateriales in listaPreguntas2BasicoMateriales:
        tipoEjercicio[int(objPreguntas2BasicoMateriales.npregunta)] = int(objPreguntas2BasicoMateriales.tipo_ejercicio)

    for npregunta in range(1, Totalpreguntas+1):

        # si me salto preguntas debo asumir que las omitio. el puntaje de esa pregunta es cero.
        if str(npregunta) not in request.session['listaRespuestasAlumno']:
            puntajePreguntas += 0
        else:
            # caso tipo fill.
            if tipoEjercicio[int(npregunta)] == 1:
                cantidad_intentos = len(request.session['listaRespuestasAlumno'][str(npregunta)])
                sub_total = 0
                for aprobada in request.session['listaRespuestasAlumno'][str(npregunta)].values():
                    sub_total += float(aprobada)
                puntajePreguntas += (sub_total/cantidad_intentos)

            # caso seleccion multiple
            if tipoEjercicio[int(npregunta)] == 2:
                cantidad_intentos = len(request.session['listaRespuestasAlumno'][str(npregunta)])
                # consulto aprobada del ultimo intento
                if request.session['listaRespuestasAlumno'][str(npregunta)][str(cantidad_intentos)] == 0:
                    puntajePreguntas += 0
                else:
                    puntajePreguntas += (1/cantidad_intentos)

            # caso seleccion multiple.
            if tipoEjercicio[int(npregunta)] == 3:
                cantidad_intentos = len(request.session['listaRespuestasAlumno'][str(npregunta)])
                # consulto aprobada del ultimo intento
                if request.session['listaRespuestasAlumno'][str(npregunta)][str(cantidad_intentos)] == 0:
                    puntajePreguntas += 0
                else:
                    puntajePreguntas += (1 / cantidad_intentos)


    puntajeActividad = redondeo((puntajePreguntas / Totalpreguntas) * 100)

    if puntajeActividad == 0:
        puntajeActividad = 1

    data = {
        'codguia': objGuias[0].codguia,
        'descguia': objGuias[0].descguia,
        'puntajeActividad': puntajeActividad,
    }


    return render(request, 'visorA2Tutor/portadaFinalModoAlumno.html', data)

def portadaFinalModoTutor(request):

    if "rut_tutor" not in request.session:
        return HttpResponse('la sesion ha caducado.')

    bd = 'materiales'
    modulo = request.session['modulo']
    objGuias = Guias.objects.using(bd).filter(codguia=modulo)
    puntajePreguntas = 0

    # consultar total de preguntas de la actividad y tipo de pregunta
    listaPreguntas2BasicoMateriales = Preguntas2BasicoMateriales.objects.using(bd).filter(idguia=int(objGuias[0].idguia))
    Totalpreguntas = len(listaPreguntas2BasicoMateriales)
    tipoEjercicio = {}

    for objPreguntas2BasicoMateriales in listaPreguntas2BasicoMateriales:
        tipoEjercicio[int(objPreguntas2BasicoMateriales.npregunta)] = int(objPreguntas2BasicoMateriales.tipo_ejercicio)

    for npregunta in range(1, Totalpreguntas+1):

        # si me salto preguntas debo asumir que las omitio. el puntaje de esa pregunta es cero.
        if str(npregunta) not in request.session['listaRespuestasAlumno']:
            puntajePreguntas += 0
        else:
            # caso tipo fill.
            if tipoEjercicio[int(npregunta)] == 1:
                cantidad_intentos = len(request.session['listaRespuestasAlumno'][str(npregunta)])
                sub_total = 0
                for aprobada in request.session['listaRespuestasAlumno'][str(npregunta)].values():
                    sub_total += float(aprobada)
                puntajePreguntas += (sub_total/cantidad_intentos)

            # caso seleccion multiple
            if tipoEjercicio[int(npregunta)] == 2:
                cantidad_intentos = len(request.session['listaRespuestasAlumno'][str(npregunta)])
                # consulto aprobada del ultimo intento
                if request.session['listaRespuestasAlumno'][str(npregunta)][str(cantidad_intentos)] == 0:
                    puntajePreguntas += 0
                else:
                    puntajePreguntas += (1/cantidad_intentos)

            # caso seleccion multiple.
            if tipoEjercicio[int(npregunta)] == 3:
                cantidad_intentos = len(request.session['listaRespuestasAlumno'][str(npregunta)])
                # consulto aprobada del ultimo intento
                if request.session['listaRespuestasAlumno'][str(npregunta)][str(cantidad_intentos)] == 0:
                    puntajePreguntas += 0
                else:
                    puntajePreguntas += (1 / cantidad_intentos)


    puntajeActividad = redondeo((puntajePreguntas / Totalpreguntas) * 100)

    if puntajeActividad == 0:
        puntajeActividad = 1

    data = {
        'codguia': objGuias[0].codguia,
        'descguia': objGuias[0].descguia,
        'puntajeActividad': puntajeActividad,
    }

    return render(request, 'visorA2Tutor/portadaFinalModoTutor.html', data)

def cerrarSesion(request):
    # cierra la sesion actual.
    logout(request)
    return HttpResponse('sesion cerrada.')

def iniciar(request):
    return render(request, 'visorA2Tutor/prueba.html')

