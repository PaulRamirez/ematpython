var imagenSolucion='';
var aprobada = 0;
var maximo_intento;
var nvuelta;
var intento=0;

$(window).on('load', function (e) {
    $(".carga").fadeOut("slow");
});

$( document ).ready(function() {

    nvuelta = $("#nvuelta").val();
    maximo_intento = $("#maximo_intento").val();

    $('.page-number').tooltip();

    $('#botonVolverVisorEvaluacion').on('click', function(e){
        $(location).attr('href','/ggalbas/contenidosAlumno');
    });


    $('#botonAvanzarEjercicio').on('click', function(e){

        e.preventDefault();
        e.stopImmediatePropagation();
        $( "#botonAvanzarEjercicio").addClass('disabled');

        if(nvuelta==1){
            guardarModoEvaluacion();
        }

        if(nvuelta==2){
            guardarModoAprendizaje();
        }

    });

    $('#botonAceptarModal').on('click', function(e){
       guardaRespuesta();
    });

    $('#botonAvanzarSolucionEjercicio').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $(location).attr('href','visorEvaluacion');
    });

    $('#parlanteEjercicio').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $('#audioEjercicio')[0].load();
        $('#audioEjercicio')[0].play();
    });

    $('#parlanteSolucionEjercicio').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $('#audioSolucionEjercicio')[0].load();
        $('#audioSolucionEjercicio')[0].play();
    });


    //teclado virtual para una resolucion pequeña por ejemplo celulares, iphone, tablet, ipad.

    var fillFocus = $('.input_fill').first(); // posiciono el foco en el primer elemento de tipo fill (completar).

    $('.input_fill').on('click', function(){
       fillFocus = $(this);
    });

    $('.tecladoVirtual').on('click', function(){    // usando el teclado virtual.
        var simbolo = $(this).text().trim();
        fillFocus.val($.trim(fillFocus.val()) + simbolo);
    });

    $('#botonBorrar').on('click', function(){
      fillFocus.val($.trim(fillFocus.val()).slice(0, -1));
    });

    //detectar si la aplicacion esta ejecutandose en dispositivo movil.
    var isMobile = {
        Android: function() {
            return navigator.userAgent.match(/Android/i);
        },
        BlackBerry: function() {
            return navigator.userAgent.match(/BlackBerry/i);
        },
        iOS: function() {
            return navigator.userAgent.match(/iPhone|iPad|iPod/i);
        },
        Opera: function() {
            return navigator.userAgent.match(/Opera Mini/i);
        },
        Windows: function() {
            return navigator.userAgent.match(/IEMobile/i);
        },
        any: function() {
            return (isMobile.Android() || isMobile.BlackBerry() || isMobile.iOS() || isMobile.Opera() || isMobile.Windows());
        }
    }

    //ocultar el teclado del dispositivo movil, haciendo una trampa, es decir, en el momento que tiene foco, inmediatamente le quito el foco con blur().
    if(isMobile.any()){
        $('.input_fill').focus(function() {
          fillFocus = this;
          this.blur();
        });
    }


    // evento al abrir modal.
    $('#ModalPreguntaObligatoria').on('shown.bs.modal', function () {

        detenerAudioEjercicio();
        $('#audioPreguntaObligatoria')[0].load();
        $('#audioPreguntaObligatoria')[0].play();
    });

  // evento al abrir modal.
    $('#ModalPreguntaSinResponder').on('shown.bs.modal', function () {
         //   alert(   $(this).attr('id'));
        detenerAudioEjercicio();
        $('#audioPreguntaSinResponder')[0].load();
        $('#audioPreguntaSinResponder')[0].play();
    });

    // evento al abrir modal.
    $('#ModalIntentoFallidoPreguntaAlternativa').on('shown.bs.modal', function () {
        detenerAudioEjercicio();
        $('#audioIntentoFallidoPreguntaAlternativa')[0].load();
        $('#audioIntentoFallidoPreguntaAlternativa')[0].play();
    });

    // evento al abrir modal.
    $('#ModalUltimoIntentoFallidoPreguntaAlternativas').on('shown.bs.modal', function () {
        detenerAudioEjercicio();
        $('#audioUltimoIntentoFallidoAlternativa')[0].load();
        $('#audioUltimoIntentoFallidoAlternativa')[0].play();
    });

    // evento al abrir modal.
    $('#ModalIntentoFallidoPreguntaFill').on('shown.bs.modal', function () {
        detenerAudioEjercicio();
        $('#audioIntentoFallidoPreguntaFill')[0].load();
        $('#audioIntentoFallidoPreguntaFill')[0].play();
    });

    // evento al abrir modal.
    $('#ModalUltimoIntentoFallidoPreguntaFill').on('shown.bs.modal', function () {
        detenerAudioEjercicio();
        $('#audioUltimoIntentoFallidoPreguntaFill')[0].load();
        $('#audioUltimoIntentoFallidoPreguntaFill')[0].play();
    });

    // envento al cerrar el modal.
    $('#ModalPreguntaObligatoria').on('hidden.bs.modal', function (e) {
        $('#audioPreguntaObligatoria')[0].load();
    });

    // envento al cerrar el modal.
    $('#ModalPreguntaSinResponder').on('hidden.bs.modal', function (e) {
        $('#audioPreguntaSinResponder')[0].load();
    });

    // envento al cerrar el modal.
    $('#ModalIntentoFallidoPreguntaAlternativa').on('hidden.bs.modal', function (e) {
        $('#audioIntentoFallidoPreguntaAlternativa')[0].load();
    });

    // envento al cerrar el modal.
    $('#ModalUltimoIntentoFallidoPreguntaAlternativas').on('hidden.bs.modal', function (e) {
        $('#audioUltimoIntentoFallidoAlternativa')[0].load();
    });

    // envento al cerrar el modal.
    $('#ModalIntentoFallidoPreguntaFill').on('hidden.bs.modal', function (e) {
        $('#audioIntentoFallidoPreguntaFill')[0].load();
    });

    // envento al cerrar el modal.
    $('#ModalUltimoIntentoFallidoPreguntaFill').on('hidden.bs.modal', function (e) {
       $('#audioUltimoIntentoFallidoPreguntaFill')[0].load();
    });

});
function guardarModoEvaluacion(){

      var preguntaSinContestar = validarPreguntaSinResponder();

      if(preguntaSinContestar==true){
            $('#ModalPreguntaSinResponder').modal('show');
            $( "#botonAvanzarEjercicio").removeClass('disabled');
        }else{
            guardaRespuesta();
        }

}

function guardarModoAprendizaje(){

    var preguntaSinContestar = validarPreguntaSinResponder();

   if(preguntaSinContestar==true){

        $('#ModalPreguntaObligatoria').modal('show');
        $( "#botonAvanzarEjercicio").removeClass('disabled');

   }else{

        if(intento < maximo_intento ){
                guardaRespuesta();
         }

        if(intento == maximo_intento && imagenSolucion == ''){
           avanzarSiguienteEjercicio();
         }

         if(intento == maximo_intento && imagenSolucion != ''){
           mostrarSolucionEjercicio();
         }

    }

}

function guardaRespuesta(){

    respuestaAlumno = obtenerRespuestaAlumno();

        $.ajax({
            async: true,
            type: "POST",
            url: "guardaRespuestaVisorEvaluacion",
            dataType: 'json',
            data: {
                'id_alumno_actividad': $('#id_alumno_actividad').val(),
                'total_ejercicios': $('#total_ejercicios').val(),
                'npregunta': $('#npregunta').val(),
                'tipo_ejercicio': $('#tipo_ejercicio').val(),
                'num_campos_completar': $('#num_campos_completar').val(),
                'nvuelta': $('#nvuelta').val(),
                'maximo_intento': $('#maximo_intento').val(),
                'respuestaAlumno': respuestaAlumno
              },
            success:function(response){

                // si se guardo correctamente la respuesta
                if(parseInt(response.estatus)==1){

                    if(nvuelta==1){

                        if(parseInt($('#npregunta').val()) < parseInt($('#total_ejercicios').val()) ){
                            avanzarSiguienteEjercicio();
                        }


                        if(parseInt($('#npregunta').val()) == parseInt($('#total_ejercicios').val())){

                            if(parseInt($("#intento_actividad").val())==1){   // primer intento de la actividad

                                if(parseFloat(response.puntajeActividad) >= 1 && parseFloat(response.puntajeActividad) < 65){
                                    avanzarPortadaFinal();
                                }
                                if(parseFloat(response.puntajeActividad) >= 65 && parseFloat(response.puntajeActividad) < 100){
                                    avanzarPortadaIntermedia();
                                }
                                if(parseFloat(response.puntajeActividad) == 100 ){
                                     avanzarPortadaFinal();
                                }

                            }

                            if(parseInt($("#intento_actividad").val())==2){   // segundo intento de la actividad

                                 if(parseFloat(response.puntajeActividad) >= 1 && parseFloat(response.puntajeActividad) < 50){
                                    avanzarPortadaFinal();
                                }

                                if(parseFloat(response.puntajeActividad) >= 50 && parseFloat(response.puntajeActividad) < 65){
                                    avanzarPortadaIntermedia();
                                }

                                if(parseFloat(response.puntajeActividad) >= 65 && parseFloat(response.puntajeActividad) < 100){
                                     avanzarPortadaIntermedia();
                                }

                                if(parseFloat(response.puntajeActividad) == 100 ){
                                     avanzarPortadaFinal();
                                }

                            }

                            if(parseInt($("#intento_actividad").val())==3){   // tercer intento de la actividad

                                if(parseFloat(response.puntajeActividad) >= 1 && parseFloat(response.puntajeActividad) < 50){
                                    avanzarPortadaIntermedia();
                                }
                                if(parseFloat(response.puntajeActividad) >= 50 && parseFloat(response.puntajeActividad) < 65){
                                    avanzarPortadaIntermedia();
                                }
                                if(parseFloat(response.puntajeActividad) >= 65 && parseFloat(response.puntajeActividad) < 100){
                                     avanzarPortadaIntermedia();
                                }
                                if(parseFloat(response.puntajeActividad) == 100 ){
                                     avanzarPortadaFinal();
                                }
                            }

                        }

                    }

                    if(nvuelta==2){

                        aprobada = parseFloat(response.aprobada)      // set variables globales.
                        intento = parseInt(response.intento)

                        if(aprobada == 1 && response.solucion_imagen != ''){

                            imagenSolucion = response.solucion_imagen;
                            mostrarSolucionEjercicio();
                        }

                        if(aprobada == 1 && response.solucion_imagen == ''){
                                avanzarSiguienteEjercicio();
                        }

                        if(aprobada < 1 && intento < maximo_intento){

                            if(parseInt($('#tipo_ejercicio').val())== 1){

                                $('#ModalIntentoFallidoPreguntaFill').modal('show');            // modal mensaje de intento fallido.

                                $(".input_fill").css("color", "");                              // remover los colores.
                                listaCondicionFill = response.listaCondicionFill
                                $(".input_fill").each(function (index) {                        // colocar en color rojo a las alternativas incorrectas
                                   if(listaCondicionFill[index]=='incorrecto'){                 // bloquear las alternativas contestadas correctamente.
                                        $(this).css("color", "red");
                                   }else{
                                        $(this).attr('disabled', true);
                                        $(this).css("color", "green");
                                   }
                                });

                                $( "#botonAvanzarEjercicio").removeClass('disabled');

                            }

                            else if(parseInt($('#tipo_ejercicio').val())== 2){                  // seleccion unica.

                                $('#ModalIntentoFallidoPreguntaAlternativa').modal('show');    // modal mensaje de intento fallido.

                                 $('.input_radio').prop('checked', false);                      // desclick a todas las alternativas.

                                 $( "#botonAvanzarEjercicio").removeClass('disabled');

                            }

                            else if(parseInt($('#tipo_ejercicio').val())== 3){

                                $('#ModalIntentoFallidoPreguntaAlternativa').modal('show');     // modal mensaje de intento fallido.

                                $('.input_checkbox').prop('checked', false);                    // desclick a todas las alternativas.

                                $( "#botonAvanzarEjercicio").removeClass('disabled');

                            }

                        }

                        if(aprobada < 1 && intento == maximo_intento){

                            imagenSolucion = response.solucion_imagen;

                            if(parseInt($('#tipo_ejercicio').val())== 1){                               // tipo fill.

                                $('#ModalUltimoIntentoFallidoPreguntaFill').modal('show');              // modal mensaje de ultimo intento fallido.

                                array_respuesta_correcta = response.respuesta_correcta.split('~')
                                                                                                        // colocar la respuesta correcta y color verde en alternativas fallidas.
                                $(".input_fill").each(function (index) {                                // bloquear todas las alternativas.
                                    $(this).css("color", "green").val(array_respuesta_correcta[index]);
                                    $(this).attr('disabled', true);
                                });

                                $( "#botonAvanzarEjercicio").removeClass('disabled');

                            }

                            else if(parseInt($('#tipo_ejercicio').val())== 2){                         // tipo seleccion unica.

                                $('#ModalUltimoIntentoFallidoPreguntaAlternativas').modal('show');      // modal mensaje de ultimo intento fallido.

                                $('.input_radio').prop('checked', false);                               // desclick a todas las alternativas.

                                respuesta_correcta = response.respuesta_correcta;      // bloquear solo las alternativas incorrectas.

                                $(".input_radio").each(function (index) {
                                    if($(this).val() != respuesta_correcta) {
                                         $(this).attr('disabled', true);
                                    }
                                });

                                $( "#botonAvanzarEjercicio").removeClass('disabled');

                            }

                            else if(parseInt($('#tipo_ejercicio').val())== 3){                         // tipo seleccion multiple.

                                $('#ModalUltimoIntentoFallidoPreguntaAlternativas').modal('show');     // modal mensaje de ultimo intento fallido.

                                $('.input_checkbox').prop('checked', false);                            // // desclick a todas las alternativas.

                                array_respuesta = response.respuesta_correcta.split('~');
                                respuesta_incorrrecta = array_respuesta[1];
                                array_respuesta_incorrecta = respuesta_incorrrecta.split('');

                                $.each(array_respuesta_incorrecta, function (ind, elem) {
                                    $('#checkbox-'+elem).attr('disabled', true);
                                });

                                $( "#botonAvanzarEjercicio").removeClass('disabled');

                            }

                         }

                    }

                }

                else if (parseInt(response.estatus)==0){
                     console.log(response.mensaje)
                     // mostrar modal amigable de error.
                     $( "#botonAvanzarEjercicio").removeClass('disabled');
                }

            }

        });



}

function mostrarSolucionEjercicio(){

     $("#imagenSolucionEjercicio").attr("src", "data:;base64,"+imagenSolucion);

     $("#divVisorEjercicio").hide();
     $("#divSolucionEjercicio").show();
     detenerAudioEjercicio();
     if(parseInt($("#numero_nivel").val())==3 || parseInt($("#numero_nivel").val())==4){
        $("#src_ogg_solucion_ejercicio").attr("src", static_url+"core/audios/e_test/"+$("#nombre_actividad").val().toLowerCase()+"_e"+$("#npregunta").val()+"_pop.ogg");
        $("#src_mp3_solucion_ejercicio").attr("src", static_url+"core/audios/e_test/"+$("#nombre_actividad").val().toLowerCase()+"_e"+$("#npregunta").val()+"_pop.mp3");
        $('#audioSolucionEjercicio')[0].load();
        $('#audioSolucionEjercicio')[0].play();
     }

}

function detenerAudioEjercicio(){

   // si el audio del ejercicio esta escuchandose, entonces lo detengo.
    if($('#audioEjercicio')[0].currentTime > 0 && !($('#audioEjercicio')[0].ended)){
        $('#audioEjercicio')[0].autoplay = false;
        $('#audioEjercicio')[0].load();
    }

}

function avanzarSiguienteEjercicio(){
    $(location).attr('href','visorEvaluacion');
}

function avanzarPortadaIntermedia(){
    $(location).attr('href','portadaIntermediaEvaluacion');
}

function avanzarPortadaFinal(){
    $(location).attr('href','portadaFinalEvaluacion');
}

function validarPreguntaSinResponder(){

    var preguntaSinContestar=false;

    if (parseInt($('#tipo_ejercicio').val()) == 1) {      // si el ejercicio es de tipo fill
        // recorre cada una de las opciones de respuesta
        $(".input_fill").each(function (index) {
            if($(this).val().trim()==''){
                preguntaSinContestar = true;  // el alumno no responde a una opcion.
                return false;
            }
        });
    }

    else  if (parseInt($('#tipo_ejercicio').val()) == 2) {

        if (parseInt($('.input_radio:checked').length) < 1 ){
            preguntaSinContestar = true;
        }

    }

    else  if (parseInt($('#tipo_ejercicio').val()) == 3) {

        if (parseInt($('.input_checkbox:checked').length) < 1 ){
            preguntaSinContestar = true;
        }

    }

    return preguntaSinContestar;
}

function obtenerRespuestaAlumno(){

    respuestaAlumno = '';

    if(parseInt($('#tipo_ejercicio').val()) == 1) {          // si el ejercicio es de tipo fill.

            $(".input_fill").each(function (index) {

                inputFill = $(this).val().trim();
                if(inputFill==''){
                    inputFill='null';
                }

                if(respuestaAlumno == ''){
                    respuestaAlumno = inputFill;
                }else{
                    respuestaAlumno += "~" + inputFill;
                }

            });

        }

    else if(parseInt($('#tipo_ejercicio').val()) == 2){

        if (parseInt($('.input_radio:checked').length) < 1 ){
            respuestaAlumno = ''
        }else{
            respuestaAlumno = $("input[name='inputRadio']:checked").val();
        }

    }

    else if (parseInt($('#tipo_ejercicio').val()) == 3) {

         if (parseInt($('.input_checkbox:checked').length) < 1 ){
                respuestaAlumno ='';
         }
         else{

                var alternativaA = '', alternativaB = '', alternativaC ='', alternativaD ='', alternativaE ='', alternativaF = '', alternativaG ='', alternativaH ='';

                $(".input_checkbox").each(function (index) {

                if($(this).is(':checked')) {

                    if($(this).val() == 'A'){
                        alternativaA += 'A';
                    }
                    if($(this).val() == 'B'){
                        alternativaB += 'B';
                    }
                    if($(this).val() == 'C'){
                        alternativaC += 'C';
                    }
                    if($(this).val() == 'D'){
                        alternativaD += 'D';
                    }
                    if($(this).val() == 'E'){
                        alternativaE += 'E';
                    }
                    if($(this).val() == 'F'){
                        alternativaF += 'F';
                    }
                    if($(this).val() == 'G'){
                        alternativaG += 'G';
                    }
                    if($(this).val() == 'H'){
                        alternativaH += 'H';
                    }
                }
            });

                respuestaAlumno = alternativaA + alternativaB + alternativaC + alternativaD + alternativaE + alternativaF + alternativaG + alternativaH;

            }
    }

    return respuestaAlumno;
}