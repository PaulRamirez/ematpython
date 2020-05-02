from django.urls import path

from . import views

urlpatterns = [

    path('iniciar', views.iniciar, name='iniciar'),

    path('rut/<slug:rut>/modulo/<slug:modulo>', views.portadaInicialModoAlumno, name='portadaInicialModoAlumno'),
    path('modo-alumno/ejercicios', views.visorModoAlumno, name='visorModoAlumno'),
    path('modo-alumno/guardarPregunta', views.guardaRespuestaModoAlumno, name='guardaRespuestaModoAlumno'),
    path('modo-alumno/resultado', views.portadaFinalModoAlumno, name='portadaFinalModoAlumno'),
    path('modo-alumno/irPantallaEjercicio', views.irPantallaEjercicio, name='irPantallaEjercicio'),
    path('modo-alumno/irPantallaPop', views.irPantallaPop, name='irPantallaPop'),
    path('modo-alumno/terminoActividad', views.terminoActividad, name='terminoActividad'),
    path('modo-alumno/buscarImagenSolucionEjercicio', views.buscarImagenSolucionEjercicio, name='buscarImagenSolucionEjercicio'),
    path('modo-alumno/cerrarSesion', views.cerrarSesion, name='cerrarSesion'),

    path('modo-tutor/rut/<slug:rut>/modulo/<slug:modulo>', views.portadaInicialModoTutor, name='portadaInicialModoTutor'),
    path('modo-tutor/ejercicios', views.visorModoTutor, name='visorModoTutor'),
    path('modo-tutor/guardarPregunta', views.guardaRespuestaModoTutor, name='guardaRespuestaModoTutor'),
    path('modo-tutor/resultado', views.portadaFinalModoTutor, name='portadaFinalModoTutor'),
    path('modo-tutor/irPantallaEjercicio', views.irPantallaEjercicio, name='irPantallaEjercicio'),
    path('modo-tutor/irPantallaPop', views.irPantallaPop, name='irPantallaPop'),
    path('modo-tutor/terminoActividad', views.terminoActividad, name='terminoActividad'),
    path('modo-tutor/buscarImagenSolucionEjercicio', views.buscarImagenSolucionEjercicio, name='buscarImagenSolucionEjercicio'),
    path('modo-tutor/cerrarSesion', views.cerrarSesion, name='cerrarSesion'),

  ]
