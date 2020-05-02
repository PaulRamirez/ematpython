from django.db import models

""""
Base de Datos e_test
"""


class Asignatura(models.Model):
    asig_id = models.AutoField(primary_key=True)
    asig_nombre = models.CharField(unique=True, max_length=45)
    asig_descripcion = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'asignatura'


class Auditoria(models.Model):
    datetime = models.DateTimeField()
    programa = models.CharField(max_length=80, blank=True, null=True)
    usuario = models.CharField(max_length=80, blank=True, null=True)
    accion = models.CharField(max_length=80, blank=True, null=True)
    tabla = models.CharField(max_length=80, blank=True, null=True)
    campo = models.CharField(max_length=80, blank=True, null=True)
    keyvalue = models.TextField(blank=True, null=True)
    oldvalue = models.TextField(blank=True, null=True)
    newvalue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditoria'


class Configuracion(models.Model):
    clave = models.CharField(primary_key=True, max_length=100)
    valor = models.CharField(max_length=255)
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'configuracion'


class Encuestas(models.Model):
    codprueba = models.CharField(primary_key=True, max_length=20)
    fecha_apertura = models.DateField()
    toma = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'encuestas'


class Objetivos(models.Model):
    objcodigo = models.AutoField(primary_key=True)
    objnombre = models.CharField(unique=True, max_length=100)
    objdescripcion = models.CharField(max_length=255)
    objtiene_subvalor = models.IntegerField()
    orden_despliegue = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objetivos'


class Objetivossubvalores(models.Model):
    idobjetivosubvalor = models.AutoField(primary_key=True)
    objcodigo = models.IntegerField()
    idobjetivovalor = models.IntegerField()
    objsubvalor = models.CharField(max_length=255)
    orden_despliegue = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objetivossubvalores'
        unique_together = (('objcodigo', 'idobjetivovalor', 'objsubvalor'),)


class Objetivosvalores(models.Model):
    idobjetivovalor = models.AutoField(primary_key=True)
    objcodigo = models.IntegerField()
    objvalor = models.CharField(max_length=255)
    orden_despliegue = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'objetivosvalores'
        unique_together = (('objcodigo', 'objvalor'),)


class Portadas(models.Model):
    tipoactividad = models.CharField(primary_key=True, max_length=20)
    nivel = models.IntegerField()
    etapa = models.IntegerField()
    portada = models.TextField(blank=True, null=True)
    portada_tipo = models.CharField(max_length=45, blank=True, null=True)
    portada_ancho = models.PositiveIntegerField(blank=True, null=True)
    portada_alto = models.PositiveIntegerField(blank=True, null=True)
    portada_tamano = models.PositiveIntegerField(blank=True, null=True)
    s_portada = models.TextField()
    s_portada_tipo = models.CharField(max_length=45, blank=True, null=True)
    s_portada_ancho = models.IntegerField(blank=True, null=True)
    s_portada_alto = models.IntegerField(blank=True, null=True)
    s_portada_tamano = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'portadas'
        unique_together = (('tipoactividad', 'nivel', 'etapa'),)


class Preguntas(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    descpregunta = models.TextField()
    alternativa1 = models.TextField()
    alternativa2 = models.TextField()
    alternativa3 = models.TextField()
    alternativa4 = models.TextField()
    alternativa5 = models.TextField()
    imagen = models.TextField(blank=True, null=True)
    idprueba = models.IntegerField()
    tipo_ejercicio = models.IntegerField()
    num_campos_completar = models.IntegerField()
    imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField()
    imagen_alto = models.IntegerField(blank=True, null=True)
    imagen_ancho = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preguntas'
        unique_together = (('npregunta', 'idprueba'),)


class Preguntas2Basico(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    idprueba = models.IntegerField()
    descpregunta = models.TextField(blank=True, null=True)
    alternativa1 = models.TextField(blank=True, null=True)
    alternativa2 = models.TextField(blank=True, null=True)
    alternativa3 = models.TextField(blank=True, null=True)
    alternativa4 = models.TextField(blank=True, null=True)
    alternativa5 = models.TextField(blank=True, null=True)
    alternativa6 = models.TextField(blank=True, null=True)
    alternativa7 = models.TextField(blank=True, null=True)
    alternativa8 = models.TextField(blank=True, null=True)
    imagen = models.TextField(blank=True, null=True)
    solucion_texto = models.TextField(blank=True, null=True)
    solucion_imagen = models.TextField(blank=True, null=True)
    tipo_ejercicio = models.IntegerField()
    num_campos_completar = models.IntegerField()
    imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    solucion_imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    imagen_alto = models.IntegerField(blank=True, null=True)
    imagen_ancho = models.IntegerField(blank=True, null=True)
    solucion_imagen_alto = models.IntegerField(blank=True, null=True)
    solucion_imagen_ancho = models.IntegerField(blank=True, null=True)
    imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    imagen_tamano = models.IntegerField(blank=True, null=True)
    solucion_imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    solucion_imagen_tamano = models.IntegerField(blank=True, null=True)
    posiciones_botones = models.CharField(max_length=250, blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField()
    s_imagen = models.TextField(blank=True, null=True)
    s_imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    s_imagen_alto = models.IntegerField(blank=True, null=True)
    s_imagen_ancho = models.IntegerField(blank=True, null=True)
    s_imagen_tamano = models.IntegerField(blank=True, null=True)
    s_solucion_imagen = models.TextField(blank=True, null=True)
    s_solucion_imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    s_solucion_imagen_alto = models.IntegerField(blank=True, null=True)
    s_solucion_imagen_ancho = models.IntegerField(blank=True, null=True)
    s_solucion_imagen_tamano = models.IntegerField(blank=True, null=True)
    alternativa9 = models.TextField(blank=True, null=True)
    alternativa10 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preguntas2basico'
        unique_together = (('npregunta', 'idprueba'),)


class PreguntasInstancias(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    npregunta = models.IntegerField()
    ninstancias = models.IntegerField()
    instancia1 = models.TextField(blank=True, null=True)
    instancia2 = models.TextField(blank=True, null=True)
    instancia3 = models.TextField(blank=True, null=True)
    instancia4 = models.TextField(blank=True, null=True)
    instancia5 = models.TextField(blank=True, null=True)
    nitemsintancias = models.IntegerField()
    instancia6 = models.TextField(blank=True, null=True)
    instancia7 = models.TextField(blank=True, null=True)
    instancia8 = models.TextField(blank=True, null=True)
    instancia9 = models.TextField(blank=True, null=True)
    instancia10 = models.TextField(blank=True, null=True)
    instancia11 = models.TextField(blank=True, null=True)
    instancia12 = models.TextField(blank=True, null=True)
    respuesta_pregunta = models.TextField()
    fecha_ultima_modificacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'preguntas_instancias'
        unique_together = (('idprueba', 'npregunta'),)


class PreguntasRecomendacion(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    npregunta = models.IntegerField()
    recomendacion = models.TextField()

    class Meta:
        managed = False
        db_table = 'preguntas_recomendacion'
        unique_together = (('idprueba', 'npregunta'),)


class Preguntasobjetivos(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    npregunta = models.IntegerField()
    objcodigo = models.IntegerField()
    idobjetivovalor = models.IntegerField()
    idobjetivosubvalor = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'preguntasobjetivos'
        unique_together = (('idprueba', 'npregunta', 'objcodigo', 'idobjetivovalor', 'idobjetivosubvalor'),)


class Pruebas(models.Model):
    codprueba = models.CharField(unique=True, max_length=20, blank=True, null=True)
    descprueba = models.CharField(max_length=45)
    npreguntas = models.IntegerField()
    idprueba = models.AutoField(primary_key=True)
    detallecontenido = models.TextField()
    tipo = models.IntegerField()
    asig_id = models.IntegerField()
    serie_id = models.IntegerField()
    vigente = models.IntegerField()
    estado = models.IntegerField()
    fecha_ultima_modificacion = models.DateTimeField()
    tipom = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pruebas'

    def __str__(self):
        return '{}'.format(self.codprueba)


class PruebasEjercicios(models.Model):
    n_pregunta = models.PositiveIntegerField()
    descripcion = models.TextField()
    eje = models.PositiveIntegerField()
    habilidad = models.PositiveIntegerField()
    cod_prueba = models.CharField(primary_key=True, max_length=45)

    class Meta:
        managed = False
        db_table = 'pruebas_ejercicios'
        unique_together = (('cod_prueba', 'n_pregunta'),)


class PruebasTipo(models.Model):
    idtipo = models.IntegerField(primary_key=True)
    descripciontipo = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'pruebas_tipo'


class Pruebasmaterial(models.Model):
    idmaterial = models.AutoField(primary_key=True)
    idprueba = models.IntegerField()
    material = models.TextField(blank=True, null=True)
    material_tipo = models.CharField(max_length=255, blank=True, null=True)
    material_tamano = models.IntegerField(blank=True, null=True)
    material_nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pruebasmaterial'


class Pruebasniveles(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    curso = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'pruebasniveles'
        unique_together = (('idprueba', 'curso'),)


class Pruebasobjetivos(models.Model):
    idprueba = models.IntegerField(primary_key=True)
    objcodigo = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'pruebasobjetivos'
        unique_together = (('idprueba', 'objcodigo'),)


class Seguridad(models.Model):
    usuario = models.CharField(primary_key=True, max_length=15)
    clave = models.CharField(max_length=15)
    userlevel = models.IntegerField(db_column='UserLevel')  # Field name made lowercase.
    nombre = models.CharField(max_length=90)

    class Meta:
        managed = False
        db_table = 'seguridad'


class Serie(models.Model):
    serie_id = models.AutoField(primary_key=True)
    serie_nombre = models.CharField(unique=True, max_length=45)
    serie_descripcion = models.TextField(blank=True, null=True)
    vigente = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'serie'


class Userlevelpermissions(models.Model):
    userlevelid = models.IntegerField(primary_key=True)
    tablename = models.CharField(max_length=80)
    permission = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'userlevelpermissions'
        unique_together = (('userlevelid', 'tablename'),)


class Userlevels(models.Model):
    userlevelid = models.IntegerField(primary_key=True)
    userlevelname = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'userlevels'


"""
Base de Datos Registromin_local 
"""

class Doc01Documentosinformes(models.Model):
    doc01_iddocumento = models.AutoField(db_column='doc01_idDocumento', primary_key=True)  # Field name made lowercase.
    doc01_tituloarchivo = models.CharField(db_column='doc01_tituloArchivo', max_length=200, blank=True, null=True)  # Field name made lowercase.
    doc01_rbd = models.CharField(max_length=100, blank=True, null=True)
    doc01_archivo = models.TextField(blank=True, null=True)
    doc01_tipo = models.CharField(max_length=50, blank=True, null=True)
    doc01_fechaultimaactualizacion = models.DateTimeField(db_column='doc01_fechaUltimaActualizacion')  # Field name made lowercase.
    doc01_usuario = models.CharField(max_length=80, blank=True, null=True)
    doc01_funciones = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'doc01_documentosinformes'


class ErrorLog(models.Model):
    iderror_log = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=45)
    modulo = models.CharField(max_length=45, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    valor = models.TextField(blank=True, null=True)
    valor_antiguo = models.TextField(blank=True, null=True)
    tipo = models.CharField(max_length=45, blank=True, null=True)
    controller = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'error_log'
        unique_together = (('iderror_log', 'rut'),)


class EstadosAlumnos(models.Model):
    institucion = models.CharField(primary_key=True, max_length=100)
    curso = models.CharField(max_length=50)
    estadonivelacion = models.IntegerField()
    mes = models.IntegerField()
    ano = models.IntegerField()
    cantidad = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'estados_alumnos'
        unique_together = (('institucion', 'curso', 'estadonivelacion', 'mes', 'ano'),)


class Ev06Registropreguntas(models.Model):
    ev03_vcrut = models.CharField(db_column='ev03_vcRut', primary_key=True, max_length=15)  # Field name made lowercase.
    ev06_inumpregunta = models.PositiveIntegerField(db_column='ev06_iNumPregunta')  # Field name made lowercase.
    ev06_dpuntaje = models.DecimalField(db_column='ev06_dPuntaje', max_digits=8, decimal_places=2, blank=True, null=True)  # Field name made lowercase.
    ev06_isubitem1 = models.PositiveIntegerField(db_column='ev06_iSubItem1', blank=True, null=True)  # Field name made lowercase.
    ev06_isubitem2 = models.PositiveIntegerField(db_column='ev06_iSubItem2', blank=True, null=True)  # Field name made lowercase.
    ev06_isubitem3 = models.PositiveIntegerField(db_column='ev06_iSubItem3', blank=True, null=True)  # Field name made lowercase.
    ev06_isubitem4 = models.PositiveIntegerField(db_column='ev06_iSubItem4', blank=True, null=True)  # Field name made lowercase.
    ev06_dfecha = models.DateTimeField(db_column='ev06_dFecha', blank=True, null=True)  # Field name made lowercase.
    ev04_vcidprueba = models.CharField(db_column='ev04_vcIdPrueba', max_length=20)  # Field name made lowercase.
    ev06_idsubitem1 = models.PositiveIntegerField(db_column='ev06_iDSubItem1', blank=True, null=True)  # Field name made lowercase.
    ev06_idsubitem2 = models.PositiveIntegerField(db_column='ev06_iDSubItem2')  # Field name made lowercase.
    ev06_idsubitem3 = models.PositiveIntegerField(db_column='ev06_iDSubItem3')  # Field name made lowercase.
    ev06_idsubitem4 = models.PositiveIntegerField(db_column='ev06_iDSubItem4')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ev06_registropreguntas'
        unique_together = (('ev03_vcrut', 'ev04_vcidprueba', 'ev06_inumpregunta'),)


class Ev07Resultados(models.Model):
    ev03_vcrut = models.CharField(db_column='ev03_vcRut', primary_key=True, max_length=20)  # Field name made lowercase.
    ev04_vcidprueba = models.CharField(db_column='ev04_vcIdPrueba', max_length=20)  # Field name made lowercase.
    ev07_dingreso = models.DateTimeField(db_column='ev07_dIngreso')  # Field name made lowercase.
    ev07_dtermino = models.DateTimeField(db_column='ev07_dTermino')  # Field name made lowercase.
    ev07_ipuntaje = models.PositiveSmallIntegerField(db_column='ev07_iPuntaje', blank=True, null=True)  # Field name made lowercase.
    ev07_vcnivellogro = models.CharField(db_column='ev07_vcNivelLogro', max_length=20, blank=True, null=True)  # Field name made lowercase.
    ev07_ih1 = models.PositiveSmallIntegerField(db_column='ev07_iH1', blank=True, null=True)  # Field name made lowercase.
    ev07_ih2 = models.PositiveSmallIntegerField(db_column='ev07_iH2', blank=True, null=True)  # Field name made lowercase.
    ev07_ih3 = models.PositiveSmallIntegerField(db_column='ev07_iH3', blank=True, null=True)  # Field name made lowercase.
    ev07_ih4 = models.PositiveSmallIntegerField(db_column='ev07_iH4', blank=True, null=True)  # Field name made lowercase.
    ev07_ieje1 = models.PositiveSmallIntegerField(db_column='ev07_iEje1', blank=True, null=True)  # Field name made lowercase.
    ev07_ieje2 = models.PositiveSmallIntegerField(db_column='ev07_iEje2', blank=True, null=True)  # Field name made lowercase.
    ev07_ieje3 = models.PositiveSmallIntegerField(db_column='ev07_iEje3')  # Field name made lowercase.
    ev07_ieje4 = models.PositiveSmallIntegerField(db_column='ev07_iEje4')  # Field name made lowercase.
    ev07_ieje5 = models.PositiveSmallIntegerField(db_column='ev07_iEje5')  # Field name made lowercase.
    ev07_ieje6 = models.PositiveSmallIntegerField(db_column='ev07_iEje6')  # Field name made lowercase.
    ev07_ieje7 = models.PositiveSmallIntegerField(db_column='ev07_iEje7')  # Field name made lowercase.
    min_ipuntaje = models.PositiveSmallIntegerField(db_column='min_iPuntaje')  # Field name made lowercase.
    min_imodo = models.PositiveSmallIntegerField(db_column='min_iModo')  # Field name made lowercase.
    min_vcmoduloini = models.CharField(db_column='min_vcModuloIni', max_length=8)  # Field name made lowercase.
    ev07_ieje8 = models.PositiveSmallIntegerField(db_column='ev07_iEje8')  # Field name made lowercase.
    ev07_ieje9 = models.PositiveSmallIntegerField(db_column='ev07_iEje9')  # Field name made lowercase.
    ev07_ieje10 = models.PositiveSmallIntegerField(db_column='ev07_iEje10')  # Field name made lowercase.
    ev07_ipuntajenivel = models.PositiveSmallIntegerField(db_column='ev07_iPuntajeNivel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ev07_resultados'
        unique_together = (('ev03_vcrut', 'ev04_vcidprueba'),)


class Ev08ResultadosFinal(models.Model):
    ev08_vcidinstitucion = models.CharField(db_column='ev08_vcIdInstitucion', primary_key=True, max_length=100)  # Field name made lowercase.
    ev08_vcidlista = models.CharField(db_column='ev08_vcIdLista', max_length=50)  # Field name made lowercase.
    ev08_vcidpruebadiag = models.CharField(db_column='ev08_vcIdPruebaDiag', max_length=20)  # Field name made lowercase.
    ev08_vcidpruebafin = models.CharField(db_column='ev08_vcIdPruebaFin', max_length=20)  # Field name made lowercase.
    ev03_vcrut = models.CharField(db_column='ev03_vcRut', max_length=20)  # Field name made lowercase.
    ev08_dfechaingreso = models.DateTimeField(db_column='ev08_dFechaIngreso')  # Field name made lowercase.
    ev08_ipuntajeprediag = models.SmallIntegerField(db_column='ev08_iPuntajePreDiag', blank=True, null=True)  # Field name made lowercase.
    ev08_ipuntajeniveldiag = models.SmallIntegerField(db_column='ev08_iPuntajeNivelDiag', blank=True, null=True)  # Field name made lowercase.
    ev08_ipuntajeprefin = models.SmallIntegerField(db_column='ev08_iPuntajePreFin', blank=True, null=True)  # Field name made lowercase.
    ev08_ipuntajenivelfin = models.SmallIntegerField(db_column='ev08_iPuntajeNivelFin', blank=True, null=True)  # Field name made lowercase.
    ev08_inumactivpre = models.SmallIntegerField(db_column='ev08_iNumActivPre', blank=True, null=True)  # Field name made lowercase.
    ev08_vcdetactivpre = models.TextField(db_column='ev08_vcDetActivPre', blank=True, null=True)  # Field name made lowercase.
    ev08_inumactivnivel = models.SmallIntegerField(db_column='ev08_iNumActivNivel', blank=True, null=True)  # Field name made lowercase.
    ev08_vcdetactivnivel = models.TextField(db_column='ev08_vcDetActivNivel', blank=True, null=True)  # Field name made lowercase.
    ev08_inotafinal = models.FloatField(db_column='ev08_iNotaFinal', blank=True, null=True)  # Field name made lowercase.
    ev08_ipuntajeprueba = models.FloatField(db_column='ev08_iPuntajePrueba', blank=True, null=True)  # Field name made lowercase.
    ev08_ipuntajenivel = models.FloatField(db_column='ev08_iPuntajeNivel', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ev08_resultados_final'
        unique_together = (('ev08_vcidinstitucion', 'ev08_vcidlista', 'ev08_vcidpruebadiag', 'ev08_vcidpruebafin', 'ev03_vcrut'),)


class FiltroCierreDiagnostico(models.Model):
    institucion = models.CharField(primary_key=True, max_length=100)
    lista = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'filtro_cierre_diagnostico'
        unique_together = (('institucion', 'lista'),)


class MaterialGuiasRespuestas(models.Model):
    codcol = models.CharField(primary_key=True, max_length=100)
    lista = models.CharField(max_length=50)
    idguia = models.IntegerField()
    npregunta = models.IntegerField()
    rut = models.CharField(max_length=15)
    respuesta = models.TextField()
    fecha = models.DateTimeField()
    instancia = models.TextField()
    respuesta_correcta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'material_guias_respuestas'
        unique_together = (('codcol', 'lista', 'idguia', 'npregunta', 'rut'),)


class MaterialGuiasResultadoAlumno(models.Model):
    codcol = models.CharField(primary_key=True, max_length=100)
    lista = models.CharField(max_length=50)
    idguia = models.IntegerField()
    rut = models.CharField(max_length=15)
    puntaje = models.FloatField()
    respuestas_buenas = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'material_guias_resultado_alumno'
        unique_together = (('codcol', 'lista', 'idguia', 'rut'),)


class MatrizCierreA3(models.Model):
    modulo = models.CharField(primary_key=True, max_length=45)
    curso_3 = models.CharField(max_length=45, blank=True, null=True)
    curso_4 = models.CharField(max_length=45, blank=True, null=True)
    curso_5 = models.CharField(max_length=45, blank=True, null=True)
    curso_6 = models.CharField(max_length=45, blank=True, null=True)
    curso_7 = models.CharField(max_length=45, blank=True, null=True)
    curso_8 = models.CharField(max_length=45, blank=True, null=True)
    curso_i = models.CharField(db_column='curso_I', max_length=45, blank=True, null=True)  # Field name made lowercase.
    curso_ii = models.CharField(db_column='curso_II', max_length=45, blank=True, null=True)  # Field name made lowercase.
    curso_iii = models.CharField(db_column='curso_III', max_length=45, blank=True, null=True)  # Field name made lowercase.
    curso_iv = models.CharField(db_column='curso_IV', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'matriz_cierre_a3'


class Min01Reporteintermedio(models.Model):
    institucion = models.CharField(primary_key=True, max_length=100)
    min01_dfechainicioactividades = models.DateField(db_column='min01_dFechaInicioActividades', blank=True, null=True)  # Field name made lowercase.
    min01_vccapacitadores = models.CharField(db_column='min01_vcCapacitadores', max_length=100)  # Field name made lowercase.
    min01_vcasistentesprimeracapacitacion = models.TextField(db_column='min01_vcAsistentesPrimeraCapacitacion')  # Field name made lowercase.
    min01_dfechaprimeracapacitacion = models.DateField(db_column='min01_dFechaPrimeraCapacitacion', blank=True, null=True)  # Field name made lowercase.
    min01_vcasistentestallertutores = models.TextField(db_column='min01_vcAsistentesTallerTutores')  # Field name made lowercase.
    min01_vcfechataller = models.CharField(db_column='min01_vcFechaTaller', max_length=100, blank=True, null=True)  # Field name made lowercase.
    min01_vcasistentescapencarmod = models.TextField(db_column='min01_vcAsistentesCapEncarMod')  # Field name made lowercase.
    min01_vcfechacapaencargadomodelo = models.CharField(db_column='min01_vcFechaCapaEncargadoModelo', max_length=100, blank=True, null=True)  # Field name made lowercase.
    min01_vcestadolaboratorio = models.TextField(db_column='min01_vcEstadoLaboratorio', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'min01_reporteintermedio'


class MinpruebasRespuestas(models.Model):
    codcol = models.CharField(primary_key=True, max_length=100)
    lista = models.CharField(max_length=50)
    idprueba = models.IntegerField()
    npregunta = models.IntegerField()
    rut = models.CharField(max_length=15)
    respuesta = models.TextField()
    fecha = models.DateTimeField()
    instancia = models.FloatField()
    respuesta_correcta = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'minpruebas_respuestas'
        unique_together = (('codcol', 'npregunta', 'idprueba', 'lista', 'rut', 'instancia'),)


class MinpruebasResultadoAlumno(models.Model):
    codcol = models.CharField(primary_key=True, max_length=100)
    lista = models.CharField(max_length=50)
    idprueba = models.IntegerField()
    rut = models.CharField(max_length=15)
    puntaje = models.FloatField()
    respuestas_buenas = models.IntegerField()
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'minpruebas_resultado_alumno'
        unique_together = (('codcol', 'lista', 'idprueba', 'rut'),)


class SisComunas(models.Model):
    comuna_id = models.AutoField(primary_key=True)
    comuna_nombre = models.CharField(max_length=64)
    provincia_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sis_comunas'


class SisProvincias(models.Model):
    provincia_id = models.AutoField(primary_key=True)
    provincia_nombre = models.CharField(max_length=64)
    region_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sis_provincias'


class SisRegiones(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_nombre = models.CharField(max_length=64)
    region_ordinal = models.CharField(max_length=4)
    zona = models.CharField(max_length=45)

    class Meta:
        managed = False
        db_table = 'sis_regiones'


class TbFechapruebas(models.Model):
    institucion = models.CharField(primary_key=True, max_length=50)
    nombreinstitucion = models.CharField(max_length=50)
    lista = models.CharField(max_length=50)
    anio = models.IntegerField()
    inicio_lista_ev1 = models.DateField(blank=True, null=True)
    fecha_lista_ev2 = models.DateField(blank=True, null=True)
    fecha_lista_ev3 = models.DateField(blank=True, null=True)
    fecha_lista_inf1 = models.DateField(blank=True, null=True)
    fecha_lista_inf2 = models.DateField(blank=True, null=True)
    fecha_lista_inf3 = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_fechapruebas'
        unique_together = (('institucion', 'lista', 'anio'),)


class TbTestvelocidad(models.Model):
    idvisita = models.AutoField(db_column='idVisita', primary_key=True)  # Field name made lowercase.
    vc_ipvisitante = models.CharField(db_column='vc_IpVisitante', max_length=45)  # Field name made lowercase.
    vc_ipvisitantereal = models.CharField(db_column='vc_IpVisitanteReal', max_length=45, blank=True, null=True)  # Field name made lowercase.
    fechavisita = models.DateTimeField(db_column='fechaVisita')  # Field name made lowercase.
    vc_sovisita = models.CharField(db_column='vc_SoVisita', max_length=45, blank=True, null=True)  # Field name made lowercase.
    idcolegiovisita = models.PositiveIntegerField(db_column='idColegioVisita', blank=True, null=True)  # Field name made lowercase.
    vc_usuariovisita = models.CharField(db_column='vc_UsuarioVisita', max_length=45, blank=True, null=True)  # Field name made lowercase.
    velocidad = models.CharField(max_length=45)
    kbenviados = models.CharField(db_column='kbEnviados', max_length=45)  # Field name made lowercase.
    tiempo = models.CharField(max_length=45)
    testsonido = models.IntegerField(db_column='testSonido')  # Field name made lowercase.
    testvideo = models.IntegerField(db_column='testVideo')  # Field name made lowercase.
    testpopup = models.IntegerField(db_column='testPopup')  # Field name made lowercase.
    equipo = models.CharField(max_length=45)
    browser = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'tb_testvelocidad'


class TblRegistroipAlumno(models.Model):
    rut = models.CharField(max_length=255)
    ip = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbl_registroip_alumno'


class TblTrabDirigido(models.Model):
    codigocol = models.CharField(primary_key=True, max_length=20)
    lista = models.CharField(max_length=20)
    f_inscripcion = models.DateTimeField()
    autorizado = models.PositiveSmallIntegerField()

    class Meta:
        managed = False
        db_table = 'tbl_trab_dirigido'
        unique_together = (('codigocol', 'lista'),)


class TblTrabDirigidoEliminado(models.Model):
    institucion = models.CharField(primary_key=True, max_length=100)
    lista = models.CharField(max_length=50)
    fecha_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbl_trab_dirigido_eliminado'
        unique_together = (('institucion', 'lista'),)


class Tblacceso(models.Model):
    rut = models.CharField(primary_key=True, max_length=16)
    nombre = models.CharField(max_length=90, blank=True, null=True)
    institucion = models.CharField(max_length=100)
    sexo = models.CharField(max_length=50, blank=True, null=True)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    curso = models.CharField(max_length=50, blank=True, null=True)
    clave = models.CharField(max_length=50, blank=True, null=True)
    tipovoz = models.IntegerField(blank=True, null=True)
    tarjeta = models.CharField(max_length=50, blank=True, null=True)
    ultimomodulo = models.CharField(max_length=50, blank=True, null=True)
    rdnat = models.IntegerField(blank=True, null=True)
    modonat = models.CharField(max_length=50, blank=True, null=True)
    modunat = models.CharField(max_length=50, blank=True, null=True)
    rddec = models.IntegerField(blank=True, null=True)
    mododec = models.CharField(max_length=50, blank=True, null=True)
    modudec = models.CharField(max_length=50, blank=True, null=True)
    rdfra = models.IntegerField(blank=True, null=True)
    modofra = models.CharField(max_length=50, blank=True, null=True)
    modufra = models.CharField(max_length=50, blank=True, null=True)
    rdent = models.IntegerField(blank=True, null=True)
    modoent = models.CharField(max_length=50, blank=True, null=True)
    moduent = models.CharField(max_length=50, blank=True, null=True)
    ruttutor = models.CharField(max_length=50, blank=True, null=True)
    fechultmod = models.CharField(db_column='fechUltMod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    penultmod = models.CharField(db_column='PenUltMod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    fechpenultmod = models.CharField(db_column='FechPenUltMod', max_length=50, blank=True, null=True)  # Field name made lowercase.
    marca = models.SmallIntegerField(blank=True, null=True)
    datosreinic = models.CharField(max_length=200, blank=True, null=True)
    habilitado = models.CharField(max_length=1, blank=True, null=True)
    madre = models.CharField(max_length=50, blank=True, null=True)
    lista = models.CharField(max_length=50, blank=True, null=True)
    fechaingreso = models.CharField(max_length=50, blank=True, null=True)
    edad = models.CharField(max_length=5, blank=True, null=True)
    colegio = models.CharField(max_length=50, blank=True, null=True)
    telefono = models.CharField(max_length=12, blank=True, null=True)
    apellidos = models.CharField(max_length=100, blank=True, null=True)
    nombres = models.TextField(blank=True, null=True)
    rdec = models.IntegerField(blank=True, null=True)
    modoec = models.CharField(max_length=50, blank=True, null=True)
    moduec = models.CharField(max_length=50, blank=True, null=True)
    ganador = models.CharField(max_length=1, blank=True, null=True)
    rdgr = models.IntegerField(blank=True, null=True)
    modogr = models.CharField(max_length=45, blank=True, null=True)
    modugr = models.CharField(max_length=45, blank=True, null=True)
    reprogramar = models.IntegerField(blank=True, null=True)
    detallereprogramacion = models.CharField(max_length=200, blank=True, null=True)
    estadonivelacion = models.PositiveIntegerField()
    detallesnivelacion = models.CharField(max_length=200)
    errores = models.TextField(blank=True, null=True)
    datosreinicmeta = models.CharField(max_length=500, blank=True, null=True)
    marcameta = models.SmallIntegerField(blank=True, null=True)
    datosreinicsep = models.CharField(max_length=500, blank=True, null=True)
    marcasep = models.SmallIntegerField(blank=True, null=True)
    marcapru = models.PositiveSmallIntegerField(blank=True, null=True)
    datosreinicpru = models.CharField(max_length=500, blank=True, null=True)
    ultima_session_id = models.TextField(blank=True, null=True)
    pregunta = models.CharField(max_length=255, blank=True, null=True)
    respuesta = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblacceso'
        unique_together = (('rut', 'institucion'),)


class TblaccesoTrabDirigido(models.Model):
    rut = models.CharField(primary_key=True, max_length=16)
    institucion = models.CharField(max_length=100)
    curso = models.CharField(max_length=50, blank=True, null=True)
    tipovoz = models.IntegerField(blank=True, null=True)
    ultimomodulo = models.CharField(max_length=50, blank=True, null=True)
    marca = models.SmallIntegerField(blank=True, null=True)
    datosreinic = models.CharField(max_length=500, blank=True, null=True)
    lista = models.CharField(max_length=50, blank=True, null=True)
    estadonivelacion = models.PositiveIntegerField()
    detallesnivelacion = models.CharField(max_length=200)
    datosreinicmeta = models.CharField(max_length=500, blank=True, null=True)
    marcameta = models.SmallIntegerField(blank=True, null=True)
    datosreinicsep = models.CharField(max_length=500, blank=True, null=True)
    marcasep = models.SmallIntegerField(blank=True, null=True)
    marcapru = models.SmallIntegerField(blank=True, null=True)
    datosreinicpru = models.CharField(max_length=500, blank=True, null=True)
    fecha_registro = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tblacceso_trab_dirigido'
        unique_together = (('rut', 'institucion'),)


class Tblcursorepaso(models.Model):
    curso = models.CharField(primary_key=True, max_length=50)
    detallerepaso = models.CharField(max_length=255)
    detallenivel = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'tblcursorepaso'


class Tbldetallecursos(models.Model):
    eje = models.CharField(primary_key=True, max_length=50)
    descripcion = models.CharField(max_length=255)
    modulo = models.CharField(max_length=50)
    tercero = models.IntegerField(blank=True, null=True)
    cuarto = models.IntegerField(blank=True, null=True)
    quinto = models.IntegerField(blank=True, null=True)
    sexto = models.IntegerField(blank=True, null=True)
    septimo = models.IntegerField(blank=True, null=True)
    octavo = models.IntegerField(blank=True, null=True)
    primero_medio = models.IntegerField(blank=True, null=True)
    segundo_medio = models.IntegerField(blank=True, null=True)
    tercero_medio = models.IntegerField(blank=True, null=True)
    cuarto_medio = models.IntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    tipoactividad = models.CharField(db_column='tipoActividad', max_length=100)  # Field name made lowercase.
    unidad = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'tbldetallecursos'
        unique_together = (('eje', 'modulo'),)


class Tbldiaslibres(models.Model):
    institucion = models.CharField(max_length=50, blank=True, null=True)
    periodo = models.IntegerField(blank=True, null=True)
    dias = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbldiaslibres'
        unique_together = (('institucion', 'periodo'),)


class Tbldistribuidores(models.Model):
    distribuidor = models.CharField(primary_key=True, max_length=50)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    telefono1 = models.CharField(max_length=50, blank=True, null=True)
    telefono2 = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    representante = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbldistribuidores'


class Tblinstituciones(models.Model):
    institucion = models.CharField(primary_key=True, max_length=50)
    nombreinstitucion = models.CharField(max_length=100, blank=True, null=True)
    director = models.CharField(max_length=50, blank=True, null=True)
    telefono1 = models.CharField(max_length=50, blank=True, null=True)
    telefono2 = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(max_length=50, blank=True, null=True)
    administrador = models.CharField(max_length=100, blank=True, null=True)
    rutadm = models.CharField(max_length=50, blank=True, null=True)
    clave = models.CharField(max_length=50, blank=True, null=True)
    preguntasecreta = models.CharField(max_length=50, blank=True, null=True)
    respuestasecreta = models.CharField(max_length=50, blank=True, null=True)
    emailadmin = models.CharField(max_length=40, blank=True, null=True)
    fechainc = models.CharField(max_length=25, blank=True, null=True)
    administradores = models.IntegerField(blank=True, null=True)
    fechacontrato = models.DateTimeField(db_column='FechaContrato', blank=True, null=True)  # Field name made lowercase.
    actualizadopor = models.CharField(db_column='Actualizadopor', max_length=100, blank=True, null=True)  # Field name made lowercase.
    tipo = models.IntegerField(blank=True, null=True)
    rbd = models.CharField(db_column='RBD', max_length=100, blank=True, null=True)  # Field name made lowercase.
    region_id = models.IntegerField(blank=True, null=True)
    provincia_id = models.IntegerField(blank=True, null=True)
    comuna_id = models.IntegerField(blank=True, null=True)
    rut_asesor = models.CharField(max_length=45, blank=True, null=True)
    nombre_asesor = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblinstituciones'


class Tbllistas(models.Model):
    institucion = models.CharField(max_length=50)
    lista = models.CharField(db_column='Lista', max_length=15)  # Field name made lowercase.
    codigolista = models.CharField(db_column='codigoLista', primary_key=True, max_length=15)  # Field name made lowercase.
    ruttutor = models.CharField(max_length=15)
    numalumnoscurso = models.PositiveIntegerField(db_column='NumAlumnosCurso')  # Field name made lowercase.
    numalumnosactivados = models.PositiveIntegerField(db_column='NumAlumnosActivados')  # Field name made lowercase.
    fecha = models.DateField()
    tipoplanificacion = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'tbllistas'


class TbllistasNotas(models.Model):
    institucion = models.CharField(primary_key=True, max_length=50)
    lista = models.CharField(max_length=15)
    codigo_lista = models.CharField(max_length=15)
    mes = models.SmallIntegerField()
    avance = models.SmallIntegerField()
    rendimiento = models.SmallIntegerField()
    indic_avance = models.SmallIntegerField()
    dificultad = models.SmallIntegerField()
    fecha_modificación = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbllistas_notas'
        unique_together = (('institucion', 'lista', 'mes'),)


class TbllistasProductosPruebas(models.Model):
    codigolista = models.CharField(db_column='codigoLista', primary_key=True, max_length=15)  # Field name made lowercase.
    prueba = models.CharField(max_length=15)
    institucion = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tbllistas_productos_pruebas'
        unique_together = (('codigolista', 'prueba'), ('codigolista', 'prueba', 'institucion'),)


class TbllistasReprogramacion(models.Model):
    institucion = models.CharField(primary_key=True, max_length=45)
    lista = models.CharField(max_length=45)
    codigo_lista = models.PositiveIntegerField(blank=True, null=True)
    correlativo = models.PositiveIntegerField(blank=True, null=True)
    unidades_reprogramadas = models.CharField(max_length=500, blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbllistas_reprogramacion'
        unique_together = (('institucion', 'lista'),)


class TbllistasRevision(models.Model):
    id_revision = models.AutoField(primary_key=True)
    institucion = models.CharField(max_length=50)
    nombreinstitucion = models.CharField(max_length=100)
    lista = models.CharField(max_length=50)
    num_alumnos_revisados = models.IntegerField()
    rut_responsable_revision = models.CharField(max_length=16)
    nombre_responsable_revision = models.CharField(max_length=100)
    fecha_revision = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbllistas_revision'


class TbllistasUnidades(models.Model):
    institucion = models.CharField(primary_key=True, max_length=50)
    lista = models.CharField(db_column='Lista', max_length=15)  # Field name made lowercase.
    codigolista = models.CharField(db_column='codigoLista', max_length=15)  # Field name made lowercase.
    codigo_unidad = models.CharField(max_length=10)
    orden = models.IntegerField()
    estado = models.IntegerField()
    fecha_ultima_modificacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tbllistas_unidades'
        unique_together = (('institucion', 'lista', 'codigolista', 'codigo_unidad'),)


class TbllistasUnidadesHistorial(models.Model):
    institucion = models.CharField(max_length=50)
    lista = models.CharField(db_column='Lista', max_length=15)  # Field name made lowercase.
    codigolista = models.CharField(db_column='codigoLista', max_length=15)  # Field name made lowercase.
    orden_unidades = models.TextField()

    class Meta:
        managed = False
        db_table = 'tbllistas_unidades_historial'


class Tbllogin(models.Model):
    rut = models.CharField(primary_key=True, max_length=30)
    fecha = models.DateTimeField()
    nivel = models.IntegerField(blank=True, null=True)
    utlimomodulo = models.CharField(max_length=45, blank=True, null=True)
    reinicio = models.CharField(max_length=300, blank=True, null=True)
    session_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbllogin'
        unique_together = (('rut', 'fecha'),)


class TblloginLocal(models.Model):
    institucion = models.CharField(max_length=100)
    rut = models.CharField(primary_key=True, max_length=30)
    fecha = models.DateTimeField()
    nivel = models.IntegerField(blank=True, null=True)
    utlimomodulo = models.CharField(max_length=45, blank=True, null=True)
    reinicio = models.CharField(max_length=300, blank=True, null=True)
    session_id = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbllogin_local'
        unique_together = (('rut', 'fecha', 'institucion'),)


class TblloginSessionMultiple(models.Model):
    rut = models.CharField(max_length=30)
    fecha = models.DateTimeField()
    reinicio = models.CharField(max_length=300, blank=True, null=True)
    session_logeado = models.TextField(blank=True, null=True)
    session_actual = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbllogin_session_multiple'


class TblloginSessionMultipleLocal(models.Model):
    institucion = models.CharField(max_length=100)
    rut = models.CharField(primary_key=True, max_length=30)
    fecha = models.DateTimeField()
    reinicio = models.CharField(max_length=300, blank=True, null=True)
    session_logeado = models.TextField(blank=True, null=True)
    session_actual = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbllogin_session_multiple_local'
        unique_together = (('rut', 'fecha', 'institucion'),)


class Tbllogros(models.Model):
    idlogro = models.IntegerField(db_column='idLogro', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=150, blank=True, null=True)
    descripcion = models.CharField(max_length=150, blank=True, null=True)
    triggerlogro = models.CharField(db_column='triggerLogro', max_length=50, blank=True, null=True)  # Field name made lowercase.
    activo = models.IntegerField(blank=True, null=True)
    medalla = models.CharField(max_length=100, blank=True, null=True)
    condicion = models.CharField(max_length=150, blank=True, null=True)
    nivelmax = models.CharField(db_column='nivelMax', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tbllogros'


class TbllogrosAlumno(models.Model):
    idlogro = models.IntegerField(primary_key=True)
    rut = models.CharField(max_length=45)
    nivel = models.IntegerField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)
    revisado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbllogros_alumno'
        unique_together = (('idlogro', 'rut'),)


class Tblmensajes(models.Model):
    idmensaje = models.CharField(max_length=50)
    desde = models.CharField(max_length=50)
    hacia = models.CharField(max_length=50)
    mensaje = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField()
    estado = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblmensajes'


class Tblobjdiag(models.Model):
    rut = models.CharField(primary_key=True, max_length=50)
    curso = models.CharField(max_length=50)
    obj1 = models.PositiveIntegerField(blank=True, null=True)
    obj2 = models.PositiveIntegerField(blank=True, null=True)
    obj3 = models.PositiveIntegerField(blank=True, null=True)
    obj4 = models.PositiveIntegerField(blank=True, null=True)
    objf1 = models.PositiveIntegerField(blank=True, null=True)
    objf2 = models.PositiveIntegerField(blank=True, null=True)
    objf3 = models.PositiveIntegerField(blank=True, null=True)
    objf4 = models.PositiveIntegerField(blank=True, null=True)
    obji1 = models.PositiveIntegerField()
    obji2 = models.PositiveIntegerField(blank=True, null=True)
    obji3 = models.PositiveIntegerField(blank=True, null=True)
    obji4 = models.PositiveIntegerField(blank=True, null=True)
    obj5 = models.PositiveIntegerField()
    objf5 = models.PositiveIntegerField(blank=True, null=True)
    obji5 = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblobjdiag'
        unique_together = (('rut', 'curso'),)


class TblproductosPruebas(models.Model):
    prueba = models.CharField(primary_key=True, max_length=15)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblproductos_pruebas'


class Tblregistro(models.Model):
    rut = models.CharField(primary_key=True, max_length=50)
    curso = models.CharField(max_length=50, blank=True, null=True)
    modulo = models.CharField(max_length=50)
    ingreso = models.DateTimeField(blank=True, null=True)
    termino = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    resultado = models.CharField(max_length=50, blank=True, null=True)
    puntaje = models.IntegerField(blank=True, null=True)
    puntajepsu = models.IntegerField(db_column='puntajePSU', blank=True, null=True)  # Field name made lowercase.
    planifsugerida = models.IntegerField(blank=True, null=True)
    planifreal = models.IntegerField(blank=True, null=True)
    hecho = models.IntegerField(blank=True, null=True)
    cuenta = models.IntegerField(blank=True, null=True)
    respaldo_reinicio = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblregistro'
        unique_together = (('rut', 'modulo'),)


class TblregistroDetalle(models.Model):
    rut = models.CharField(primary_key=True, max_length=50)
    modulo = models.CharField(max_length=50)
    correlativo = models.IntegerField()
    detalle = models.TextField(blank=True, null=True)
    fecha_termino = models.DateTimeField(blank=True, null=True)
    puntaje = models.IntegerField(blank=True, null=True)
    detalle_ejec = models.TextField(blank=True, null=True)
    puntajepsu = models.IntegerField(db_column='puntajePSU', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblregistro_detalle'
        unique_together = (('rut', 'modulo', 'correlativo'),)


class Tblrespuestas(models.Model):
    tiporesultado = models.CharField(max_length=50, blank=True, null=True)
    rut = models.CharField(primary_key=True, max_length=250)
    modulo = models.CharField(max_length=50)
    puntaje = models.IntegerField(blank=True, null=True)
    p01 = models.IntegerField(blank=True, null=True)
    p02 = models.IntegerField(blank=True, null=True)
    p03 = models.IntegerField(blank=True, null=True)
    p04 = models.IntegerField(blank=True, null=True)
    p05 = models.IntegerField(blank=True, null=True)
    p06 = models.IntegerField(blank=True, null=True)
    p07 = models.IntegerField(blank=True, null=True)
    p08 = models.IntegerField(blank=True, null=True)
    p09 = models.IntegerField(blank=True, null=True)
    p10 = models.IntegerField(blank=True, null=True)
    p11 = models.IntegerField(blank=True, null=True)
    p12 = models.IntegerField(blank=True, null=True)
    p13 = models.IntegerField(blank=True, null=True)
    p14 = models.IntegerField(blank=True, null=True)
    p15 = models.TextField(blank=True, null=True)
    p16 = models.IntegerField(blank=True, null=True)
    p17 = models.IntegerField(blank=True, null=True)
    p18 = models.IntegerField(blank=True, null=True)
    p19 = models.IntegerField(blank=True, null=True)
    p20 = models.IntegerField(blank=True, null=True)
    p21 = models.IntegerField(blank=True, null=True)
    p22 = models.IntegerField(blank=True, null=True)
    p23 = models.IntegerField(blank=True, null=True)
    p24 = models.IntegerField(blank=True, null=True)
    p25 = models.IntegerField(blank=True, null=True)
    p26 = models.IntegerField(blank=True, null=True)
    p27 = models.IntegerField(blank=True, null=True)
    p28 = models.IntegerField(blank=True, null=True)
    p29 = models.IntegerField(blank=True, null=True)
    p30 = models.IntegerField(blank=True, null=True)
    p31 = models.IntegerField(blank=True, null=True)
    p32 = models.IntegerField(blank=True, null=True)
    p33 = models.IntegerField(blank=True, null=True)
    p34 = models.IntegerField(blank=True, null=True)
    p35 = models.IntegerField(blank=True, null=True)
    p36 = models.IntegerField(blank=True, null=True)
    p37 = models.IntegerField(blank=True, null=True)
    p38 = models.IntegerField(blank=True, null=True)
    p39 = models.IntegerField(blank=True, null=True)
    p40 = models.IntegerField(blank=True, null=True)
    cuenta = models.IntegerField(blank=True, null=True)
    fechares = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblrespuestas'
        unique_together = (('rut', 'modulo'),)


class Tbltareas(models.Model):
    rut = models.CharField(primary_key=True, max_length=50)
    mes = models.IntegerField()
    modulo = models.CharField(max_length=10)
    fecha = models.DateField()
    resultado = models.IntegerField(blank=True, null=True)
    estado = models.CharField(max_length=30, blank=True, null=True)
    fechaestado = models.DateField()
    marcat = models.CharField(max_length=1, blank=True, null=True)
    datosreinict = models.CharField(max_length=200, blank=True, null=True)
    tipot = models.CharField(max_length=1, blank=True, null=True)
    fechatutor = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbltareas'
        unique_together = (('rut', 'modulo', 'fecha'),)


class Tbltareaslista(models.Model):
    institucion = models.CharField(primary_key=True, max_length=20)
    lista = models.CharField(max_length=20)
    ruttutor = models.CharField(max_length=50)
    mes = models.IntegerField()
    modulo = models.CharField(max_length=10)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbltareaslista'
        unique_together = (('institucion', 'lista', 'ruttutor', 'modulo', 'fecha'),)


class Tbltarjetas(models.Model):
    codigocolegio = models.CharField(primary_key=True, max_length=50)
    codigousuario = models.CharField(max_length=50)
    libre = models.IntegerField(blank=True, null=True)
    distribuidor = models.CharField(max_length=50, blank=True, null=True)
    tipot = models.CharField(max_length=1, blank=True, null=True)
    fecha = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbltarjetas'
        unique_together = (('codigocolegio', 'codigousuario'),)


class Tbltestrepaso(models.Model):
    numerotest = models.IntegerField(primary_key=True)
    nombretest = models.CharField(max_length=50)
    modulo1 = models.CharField(max_length=50)
    modulo2 = models.CharField(max_length=50)
    modulo3 = models.CharField(max_length=50)
    separador = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbltestrepaso'
        unique_together = (('numerotest', 'nombretest'),)


class Tbltutores(models.Model):
    institucion = models.CharField(primary_key=True, max_length=50)
    ruttutor = models.CharField(max_length=50)
    nombretutor = models.CharField(max_length=50, blank=True, null=True)
    mailtutor = models.CharField(max_length=50, blank=True, null=True)
    actualnaturales = models.CharField(max_length=15, blank=True, null=True)
    actualdecimales = models.CharField(max_length=15, blank=True, null=True)
    actualfracciones = models.CharField(max_length=15, blank=True, null=True)
    actualenteros = models.CharField(max_length=15, blank=True, null=True)
    marcanat = models.CharField(max_length=1, blank=True, null=True)
    datosreinicnat = models.CharField(max_length=200, blank=True, null=True)
    marcadec = models.CharField(max_length=1, blank=True, null=True)
    datosreinicdec = models.CharField(max_length=200, blank=True, null=True)
    marcafra = models.CharField(max_length=1, blank=True, null=True)
    datosreinicfra = models.CharField(max_length=200, blank=True, null=True)
    marcaent = models.CharField(max_length=1, blank=True, null=True)
    datosreinicent = models.CharField(max_length=200, blank=True, null=True)
    ambito = models.CharField(max_length=45, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tbltutores'
        unique_together = (('institucion', 'ruttutor'),)


class Tblunidades(models.Model):
    codigo_unidad = models.CharField(primary_key=True, max_length=10)
    nombre_unidad = models.CharField(max_length=100)
    eje_unidad = models.CharField(max_length=100)
    codprueba = models.CharField(max_length=10)
    producto = models.CharField(max_length=15)
    nivel_del_programa = models.IntegerField()
    posicion_detalle_nivel = models.IntegerField()
    tipo = models.CharField(max_length=10)
    codigo_eje = models.CharField(max_length=10)
    estado = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tblunidades'
        unique_together = (('codigo_unidad', 'producto', 'nivel_del_programa'),)


class TblunidadesActividades(models.Model):
    codigo_unidad = models.CharField(primary_key=True, max_length=10)
    codguia = models.CharField(max_length=10)
    producto = models.CharField(max_length=15)
    orden = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tblunidades_actividades'
        unique_together = (('codigo_unidad', 'codguia', 'producto'),)


class Tblusuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    id_institucion = models.CharField(max_length=50, blank=True, null=True)
    rut = models.CharField(max_length=15, blank=True, null=True)
    nombre = models.CharField(max_length=80, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=50, blank=True, null=True)  # Field renamed because it was a Python reserved word.
    pregunta = models.CharField(max_length=100, blank=True, null=True)
    respuesta = models.CharField(max_length=100, blank=True, null=True)
    ambito = models.CharField(max_length=45, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tblusuarios'


class TblvisitasTutores(models.Model):
    visita_id = models.AutoField(primary_key=True)
    visita_link_pagina = models.TextField()
    visita_titulo_pagina = models.CharField(max_length=100)
    rut = models.CharField(max_length=16)
    rbd = models.CharField(db_column='RBD', max_length=100)  # Field name made lowercase.
    lista = models.CharField(max_length=50)
    visita_fecha = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'tblvisitas_tutores'


class Unidadesrecniv(models.Model):
    producto = models.CharField(db_column='Producto', primary_key=True, max_length=15)  # Field name made lowercase.
    usounidad = models.CharField(db_column='UsoUnidad', max_length=15)  # Field name made lowercase.
    correlativo = models.PositiveIntegerField(db_column='Correlativo')  # Field name made lowercase.
    posicion = models.PositiveIntegerField(db_column='Posicion', blank=True, null=True)  # Field name made lowercase.
    activ1 = models.CharField(db_column='Activ1', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ2 = models.CharField(db_column='Activ2', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ3 = models.CharField(db_column='Activ3', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ4 = models.CharField(db_column='Activ4', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ5 = models.CharField(db_column='Activ5', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ6 = models.CharField(db_column='Activ6', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ7 = models.CharField(db_column='Activ7', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ8 = models.CharField(db_column='Activ8', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ9 = models.CharField(db_column='Activ9', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activ10 = models.CharField(db_column='Activ10', max_length=4, blank=True, null=True)  # Field name made lowercase.
    titulo = models.CharField(db_column='Titulo', max_length=80, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'unidadesrecniv'
        unique_together = (('producto', 'usounidad', 'correlativo'),)



"""
Base de Datos materiales
"""

class AuditoriaMateriales(models.Model):
    datetime = models.DateTimeField()
    programa = models.CharField(max_length=80, blank=True, null=True)
    usuario = models.CharField(max_length=80, blank=True, null=True)
    accion = models.CharField(max_length=80, blank=True, null=True)
    tabla = models.CharField(max_length=80, blank=True, null=True)
    campo = models.CharField(max_length=80, blank=True, null=True)
    keyvalue = models.TextField(blank=True, null=True)
    oldvalue = models.TextField(blank=True, null=True)
    newvalue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auditoria'


class Audittrail(models.Model):
    datetime = models.DateTimeField()
    script = models.CharField(max_length=80, blank=True, null=True)
    user = models.CharField(max_length=80, blank=True, null=True)
    action = models.CharField(max_length=80, blank=True, null=True)
    table = models.CharField(max_length=80, blank=True, null=True)
    field = models.CharField(max_length=80, blank=True, null=True)
    keyvalue = models.TextField(blank=True, null=True)
    oldvalue = models.TextField(blank=True, null=True)
    newvalue = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'audittrail'


class ConfiguracionMateriales(models.Model):
    clave = models.CharField(primary_key=True, max_length=100)
    valor = models.CharField(max_length=255)
    descripcion = models.TextField()

    class Meta:
        managed = False
        db_table = 'configuracion'


class Ejeycontenido(models.Model):
    modulo = models.CharField(primary_key=True, max_length=45)
    eje = models.CharField(max_length=45)
    contenido = models.CharField(max_length=45)
    sigla = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'ejeycontenido'


class GuiaPortadas(models.Model):
    tipoactividad = models.CharField(primary_key=True, max_length=20)
    nivel = models.IntegerField()
    portada = models.TextField(blank=True, null=True)
    portada_tipo = models.CharField(max_length=45, blank=True, null=True)
    portada_ancho = models.PositiveIntegerField(blank=True, null=True)
    portada_alto = models.PositiveIntegerField(blank=True, null=True)
    portada_tamano = models.PositiveIntegerField(blank=True, null=True)
    s_portada = models.TextField()
    s_portada_tipo = models.CharField(max_length=45, blank=True, null=True)
    s_portada_ancho = models.IntegerField(blank=True, null=True)
    s_portada_alto = models.IntegerField(blank=True, null=True)
    s_portada_tamano = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guia_portadas'
        unique_together = (('tipoactividad', 'nivel'),)


class Guias(models.Model):
    idguia = models.AutoField(primary_key=True)
    codguia = models.CharField(unique=True, max_length=20, blank=True, null=True)
    descguia = models.CharField(max_length=100)
    tipo = models.CharField(max_length=2, blank=True, null=True)
    npreguntas = models.IntegerField()
    detallecontenido = models.TextField(blank=True, null=True)
    codigotoolbook = models.CharField(unique=True, max_length=45)
    producto = models.IntegerField()
    fecha_ultima_modificacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'guias'


class Guiasmaterial(models.Model):
    idmaterial = models.AutoField(primary_key=True)
    idguia = models.IntegerField()
    material = models.TextField(blank=True, null=True)
    material_tipo = models.CharField(max_length=255, blank=True, null=True)
    material_tamano = models.IntegerField(blank=True, null=True)
    material_nombre = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'guiasmaterial'


class Guiasniveles(models.Model):
    idguia = models.IntegerField(primary_key=True)
    curso = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'guiasniveles'
        unique_together = (('idguia', 'curso'),)


class Imgpreguntasdrg(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    idguia = models.IntegerField()
    imdrg1 = models.TextField(blank=True, null=True)
    imdrg2 = models.TextField(blank=True, null=True)
    imdrg3 = models.TextField(blank=True, null=True)
    imdrg4 = models.TextField(blank=True, null=True)
    imdrg5 = models.TextField(blank=True, null=True)
    imdrg6 = models.TextField(blank=True, null=True)
    imdrg7 = models.TextField(blank=True, null=True)
    imdrg8 = models.TextField(blank=True, null=True)
    imdrg9 = models.TextField(blank=True, null=True)
    imdrg10 = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'imgpreguntasdrg'
        unique_together = (('npregunta', 'idguia'),)


class Metaguia(models.Model):
    codguia = models.CharField(primary_key=True, max_length=20)
    guias_miembro = models.CharField(max_length=100, blank=True, null=True)
    pos_botones_guias = models.CharField(max_length=80, blank=True, null=True)
    nguias_miembro = models.IntegerField()
    portada = models.TextField(blank=True, null=True)
    portada_tipo = models.CharField(max_length=45, blank=True, null=True)
    portada_ancho = models.PositiveIntegerField(blank=True, null=True)
    portada_alto = models.PositiveIntegerField(blank=True, null=True)
    portada_tamano = models.PositiveIntegerField(blank=True, null=True)
    tipo = models.CharField(max_length=1, blank=True, null=True)
    s_portada = models.TextField(blank=True, null=True)
    s_portada_tipo = models.CharField(max_length=45, blank=True, null=True)
    s_portada_ancho = models.IntegerField(blank=True, null=True)
    s_portada_alto = models.IntegerField(blank=True, null=True)
    s_portada_tamano = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'metaguia'


class PreguntasMateriales(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    idguia = models.IntegerField()
    descpregunta = models.TextField()
    alternativa1 = models.TextField()
    alternativa2 = models.TextField()
    alternativa3 = models.TextField()
    alternativa4 = models.TextField()
    alternativa5 = models.TextField()
    imagen = models.TextField(blank=True, null=True)
    solucion_texto = models.TextField(blank=True, null=True)
    solucion_imagen = models.TextField(blank=True, null=True)
    tipo_ejercicio = models.IntegerField(blank=True, null=True)
    num_campos_completar = models.IntegerField(blank=True, null=True)
    imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    solucion_imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    imagen_alto = models.IntegerField(blank=True, null=True)
    imagen_ancho = models.IntegerField(blank=True, null=True)
    solucion_imagen_alto = models.IntegerField(blank=True, null=True)
    solucion_imagen_ancho = models.IntegerField(blank=True, null=True)
    imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    imagen_tamano = models.IntegerField(blank=True, null=True)
    solucion_imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    solucion_imagen_tamano = models.IntegerField(blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'preguntas'
        unique_together = (('npregunta', 'idguia'),)


class Preguntas2BasicoMateriales(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    idguia = models.IntegerField()
    descpregunta = models.TextField(blank=True, null=True)
    alternativa1 = models.TextField(blank=True, null=True)
    alternativa2 = models.TextField(blank=True, null=True)
    alternativa3 = models.TextField(blank=True, null=True)
    alternativa4 = models.TextField(blank=True, null=True)
    alternativa5 = models.TextField(blank=True, null=True)
    alternativa6 = models.TextField(blank=True, null=True)
    alternativa7 = models.TextField(blank=True, null=True)
    alternativa8 = models.TextField(blank=True, null=True)
    imagen = models.TextField(blank=True, null=True)
    solucion_texto = models.TextField(blank=True, null=True)
    solucion_imagen = models.TextField(blank=True, null=True)
    tipo_ejercicio = models.IntegerField()
    num_campos_completar = models.IntegerField()
    imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    solucion_imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    imagen_alto = models.IntegerField(blank=True, null=True)
    imagen_ancho = models.IntegerField(blank=True, null=True)
    solucion_imagen_alto = models.IntegerField(blank=True, null=True)
    solucion_imagen_ancho = models.IntegerField(blank=True, null=True)
    imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    imagen_tamano = models.IntegerField(blank=True, null=True)
    solucion_imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    solucion_imagen_tamano = models.IntegerField(blank=True, null=True)
    posiciones_botones = models.CharField(max_length=250, blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField()
    s_imagen = models.TextField(blank=True, null=True)
    s_imagen_tipo = models.CharField(max_length=45, blank=True, null=True)
    s_imagen_alto = models.IntegerField(blank=True, null=True)
    s_imagen_ancho = models.IntegerField(blank=True, null=True)
    s_imagen_tamano = models.IntegerField(blank=True, null=True)
    s_solucion_imagen = models.TextField(blank=True, null=True)
    s_solucion_imagen_tipo = models.CharField(max_length=45, blank=True, null=True)
    s_solucion_imagen_alto = models.IntegerField(blank=True, null=True)
    s_solucion_imagen_ancho = models.IntegerField(blank=True, null=True)
    s_solucion_imagen_tamano = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preguntas2basico'
        unique_together = (('npregunta', 'idguia'),)


class PreguntasInstanciasMateriales(models.Model):
    idguia = models.IntegerField(primary_key=True)
    npregunta = models.IntegerField()
    ninstancias = models.IntegerField()
    instancia1 = models.TextField(blank=True, null=True)
    instancia2 = models.TextField(blank=True, null=True)
    instancia3 = models.TextField(blank=True, null=True)
    instancia4 = models.TextField(blank=True, null=True)
    instancia5 = models.TextField(blank=True, null=True)
    nitemsintancias = models.IntegerField()
    instancia6 = models.TextField(blank=True, null=True)
    instancia7 = models.TextField(blank=True, null=True)
    instancia8 = models.TextField(blank=True, null=True)
    instancia9 = models.TextField(blank=True, null=True)
    instancia10 = models.TextField(blank=True, null=True)
    instancia11 = models.TextField(blank=True, null=True)
    instancia12 = models.TextField(blank=True, null=True)
    respuesta_pregunta = models.TextField()
    fecha_ultima_modificacion = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'preguntas_instancias'
        unique_together = (('idguia', 'npregunta'),)


class Preguntasa4(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    idguia = models.IntegerField()
    imagen = models.TextField(blank=True, null=True)
    tipo_ejercicio = models.IntegerField(blank=True, null=True)
    num_campos_completar = models.IntegerField()
    imagen_tipo = models.CharField(max_length=100, blank=True, null=True)
    imagen_alto = models.IntegerField(blank=True, null=True)
    imagen_ancho = models.IntegerField(blank=True, null=True)
    imagen_nombre = models.CharField(max_length=100, blank=True, null=True)
    imagen_tamano = models.IntegerField(blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField()
    posiciones_botones = models.CharField(max_length=250, blank=True, null=True)
    vector_pares = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'preguntasa4'
        unique_together = (('npregunta', 'idguia'),)


class Preguntasdrg(models.Model):
    npregunta = models.IntegerField(primary_key=True)
    idguia = models.IntegerField()
    imagen = models.TextField(blank=True, null=True)
    tipo_ejercicio = models.IntegerField(blank=True, null=True)
    num_drag = models.IntegerField()
    num_targ = models.IntegerField()
    imagen_tipo = models.CharField(max_length=10, blank=True, null=True)
    imagen_alto = models.IntegerField(blank=True, null=True)
    imagen_ancho = models.IntegerField(blank=True, null=True)
    imagen_nombre = models.CharField(max_length=20, blank=True, null=True)
    imagen_tamano = models.IntegerField(blank=True, null=True)
    fecha_ultima_modificacion = models.DateTimeField()
    posiciones_botones_drg = models.CharField(max_length=250, blank=True, null=True)
    posiciones_botones_targ = models.CharField(max_length=250, blank=True, null=True)
    vector_pares_drgtg = models.CharField(max_length=500, blank=True, null=True)
    anchodrag = models.PositiveSmallIntegerField(db_column='anchoDrag', blank=True, null=True)  # Field name made lowercase.
    altodrag = models.PositiveSmallIntegerField(db_column='altoDrag', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'preguntasdrg'
        unique_together = (('npregunta', 'idguia'),)


class SeguridadMateriales(models.Model):
    usuario = models.CharField(primary_key=True, max_length=15)
    clave = models.CharField(max_length=15)
    userlevel = models.IntegerField(db_column='UserLevel')  # Field name made lowercase.
    nombre = models.CharField(max_length=90)

    class Meta:
        managed = False
        db_table = 'seguridad'


class UserlevelpermissionsMateriales(models.Model):
    userlevelid = models.IntegerField(primary_key=True)
    tablename = models.CharField(max_length=80)
    permission = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'userlevelpermissions'
        unique_together = (('userlevelid', 'tablename'),)


class UserlevelsMateriales(models.Model):
    userlevelid = models.IntegerField(primary_key=True)
    userlevelname = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'userlevels'

