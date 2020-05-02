from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('recuperaClave', views.recuperaClave, name='recuperaClave'),
    path('nuevoAlumno', views.nuevoAlumno, name='nuevoAlumno'),
    path('nuevoAlumno/agregarAlumno', views.agregarAlumno, name='agregarAlumno'),
    path('recuperaClave/verificaRut', views.verificaRut, name='verificaRut'),
    path('recuperaClave/verificaRespuesta', views.verificaRespuesta, name='verificaRespuesta'),
    path('verificaRutIp', views.verificaRutIp, name='verificaRutIp'),
    path('ingresoCompleto', views.ingresoCompleto, name='ingresoCompleto'),
    path('ingresoSoloRut', views.ingresoSoloRut, name='ingresoSoloRut'),
    path('antePortada', views.antePortada, name='antePortada'),
    path('portadaVisor', views.portadaVisor, name='portadaVisor'),
    path('visorActividades', views.visorActividades, name='visorActividades'),
    path('guardaRespuesta', views.guardaRespuesta, name='guardaRespuesta'),
    path('calculoDiagnostico', views.calculoDiagnostico, name='calculoDiagnostico'),
    path('cierreEvaluacionesAnuales', views.cierreEvaluacionesAnuales, name='cierreEvaluacionesAnuales'),
    path('portadaFinalDiagnostico', views.portadaFinalDiagnostico, name='portadaFinalDiagnostico'),
    path('obtenerIp', views.obtenerIp, name='obtenerIp'),
    path('unidadesAlumno', views.unidadesAlumno, name='unidadesAlumno'),
    path('contenidosAlumno', views.contenidosAlumno, name='contenidosAlumno'),
    path('visorActividadComp', views.visorActividadComp, name='visorActividadComp'),
    path('visorActividad', views.visorActividad, name='visorActividad'),
    path('iniciarActividad', views.iniciarActividad, name='iniciarActividad'),
    path('iniciarActividadComp', views.iniciarActividadComp, name='iniciarActividadComp'),
    path('complementariasUnidad', views.complementariasUnidad, name='complementariasUnidad'),
    path('complementariasLibre', views.complementariasLibre, name='complementariasLibre'),
    path('validarUnidadSigHabilitada', views.validarUnidadSigHabilitada, name='validarUnidadSigHabilitada'),
    path('validarActividadComplementariaIniciada', views.validarActividadComplementariaIniciada, name='validarActividadComplementariaIniciada'),
    path('validarContenidoTerminado', views.validarContenidoTerminado, name='validarContenidoTerminado'),
    path('validarAlumnoCompLibre', views.validarAlumnoCompLibre, name='validarAlumnoCompLibre'),
]

