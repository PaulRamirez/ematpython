from django.urls import path

from . import views

urlpatterns = [
    # Visor de MT
    path('portadaInicialMT', views.portadaInicialMT, name='portadaInicialMT'),
    path('visorMT', views.visorMT, name='visorMT'),
    path('guardaRespuestaMT', views.guardaRespuestaMT, name='guardaRespuestaMT'),
    path('portadaFinalMT', views.portadaFinalMT, name='portadaFinalMT'),
    # Visor de Aprendizaje
    path('portadaInicialAprendizaje', views.portadaInicialAprendizaje, name='portadaInicialAprendizaje'),
    path('visorAprendizaje', views.visorAprendizaje, name='visorAprendizaje'),
    path('guardaRespuestaVisorAprendizaje', views.guardaRespuestaVisorAprendizaje, name='guardaRespuestaVisorAprendizaje'),
    path('portadaFinalAprendizaje', views.portadaFinalAprendizaje, name='portadaFinalAprendizaje'),
    # Visor de Evaluacion
    path('portadaInicialEvaluacion', views.portadaInicialEvaluacion, name='portadaInicialEvaluacion'),
    path('visorEvaluacion', views.visorEvaluacion, name='visorEvaluacion'),
    path('guardaRespuestaVisorEvaluacion', views.guardaRespuestaVisorEvaluacion, name='guardaRespuestaVisorEvaluacion'),
    path('portadaIntermediaEvaluacion', views.portadaIntermediaEvaluacion, name='portadaIntermediaEvaluacion'),
    path('portadaFinalEvaluacion', views.portadaFinalEvaluacion, name='portadaFinalEvaluacion'),
    # Visor de Repaso
    path('portadaInicialRepaso', views.portadaInicialRepaso, name='portadaInicialRepaso'),
    path('visorRepaso', views.visorRepaso, name='visorRepaso'),
    path('guardaRespuestaVisorRepaso', views.guardaRespuestaVisorRepaso, name='guardaRespuestaVisorRepaso'),
    path('portadaFinalRepaso', views.portadaFinalRepaso, name='portadaFinalRepaso'),
    # Visor Meta
    path('portadaInicialMeta', views.portadaInicialMeta, name='portadaInicialMeta'),
    path('portadaFinalMeta', views.portadaFinalMeta, name='portadaFinalMeta'),

    # Visor de Integracion.
    path('visorIntegracion', views.visorIntegracion, name='visorIntegracion'),
  ]