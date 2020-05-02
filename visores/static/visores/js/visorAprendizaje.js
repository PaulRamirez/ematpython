var TieneMasIntentos='SI';
var Aprobada = 0;
var imagenSolucion='';


$(window).on('load', function (e) {
    $(".carga").fadeOut("slow");

});

$( document ).ready(function() {

    $('#numeroEjercicio').tooltip();

    $('#botonAvanzarEjercicio').on('click', function(e){

        e.preventDefault();
        e.stopImmediatePropagation();

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

       if(preguntaSinContestar==true){
            $('#ModalPreguntaObligatoria').modal('show');
       }else{

            if( TieneMasIntentos == 'SI' && Aprobada==0){
                guardaRespuestaVisorAprendizaje();
            }else{

                 if(imagenSolucion ==''){

                     $(location).attr('href','visorAprendizaje');

                 }else{
                     mostrarSolucionEjercicio();
                 }
            }

       }

    });

    $('#botonAvanzarSolucionEjercicio').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $(location).attr('href','visorAprendizaje');
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

function guardaRespuestaVisorAprendizaje(){

    $( "#botonAvanzarEjercicio").addClass('disabled');

    detenerAudioEjercicio();

    respuestasAlumno = '';

        if(parseInt($('#tipo_ejercicio').val()) == 1) {          // si el ejercicio es de tipo fill.

            $(".input_fill").each(function (index) {

                inputFill = $(this).val().trim();

                if(respuestasAlumno == ''){
                    respuestasAlumno = inputFill;
                }else{
                    respuestasAlumno += "~" + inputFill;
                }

            });

        }

        else if(parseInt($('#tipo_ejercicio').val()) == 2){

            inputRadio = parseInt($("input[name='inputRadio']:checked").val());
            respuestasAlumno = convertirLetra(inputRadio);

        }

        else if (parseInt($('#tipo_ejercicio').val()) == 3) {

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

            respuestasAlumno = alternativaA + alternativaB + alternativaC + alternativaD + alternativaE + alternativaF + alternativaG + alternativaH;


        }

        $.ajax({
            async: true,
            type: "POST",
            url: "guardaRespuestaVisorAprendizaje",
            dataType: 'json',
            data: {
                'id_alumno_actividad': $('#id_alumno_actividad').val(),
                'npregunta': $('#npregunta').val(),
                'tipo_ejercicio': $('#tipo_ejercicio').val(),
                'num_campos_completar': $('#num_campos_completar').val(),
                'respuestasAlumno': respuestasAlumno
              },
            success:function(response){

                $( "#botonAvanzarEjercicio").removeClass('disabled');

                // si se guardo correctamente la respuesta
                if(parseInt(response.estatus)==1){

                    Aprobada = parseInt(response.aprobada)      // set variables globales.
                    TieneMasIntentos = response.TieneMasIntentos  // set variables globales.
                    // si respondio correctamente

                    if(parseInt(response.aprobada) == 1){
                        imagenSolucion = response.solucion_imagen;
                        $( "#botonAvanzarEjercicio" ).trigger( "click" );
                    }
                     else{

                        if(response.TieneMasIntentos=='SI'){

                            if(parseInt($('#tipo_ejercicio').val())== 1){

                                $('#ModalIntentoFallidoPreguntaFill').modal('show');            // modal mensaje de intento fallido.

                                $(".input_fill").css("color", "");                              // remover los colores rojos y verdes de todas als alternativas
                                listaCondicionFill = response.listaCondicionFill
                                $(".input_fill").each(function (index) {                        // colocar en color rojo a las alternativas incorrectas
                                   if(listaCondicionFill[index]=='incorrecto'){                 // bloquear las alternativas contestadas correctamente.
                                        $(this).css("color", "red");
                                   }else{
                                        $(this).attr('disabled', true);
                                        $(this).css("color", "green");
                                   }
                                });

                            }

                            else if(parseInt($('#tipo_ejercicio').val())== 2){                  // seleccion unica.

                                 $('.input_radio').prop('checked', false);                      // desclick a todas las alternativas.
                                 $('#ModalIntentoFallidoPreguntaAlternativa').modal('show');    // modal mensaje de intento fallido.

                            }

                            else if(parseInt($('#tipo_ejercicio').val())== 3){

                                $('.input_checkbox').prop('checked', false);                    // desclick a todas las alternativas.
                                $('#ModalIntentoFallidoPreguntaAlternativa').modal('show');     // modal mensaje de intento fallido.
                            }

                        }

                        else{

                            imagenSolucion = response.solucion_imagen;

                            if(parseInt($('#tipo_ejercicio').val())== 1){                               // tipo fill.

                                $('#ModalUltimoIntentoFallidoPreguntaFill').modal('show');              // modal mensaje de ultimo intento fallido.

                                array_respuesta_correcta = response.respuesta_correcta.split('~')
                                                                                                        // colocar la respuesta correcta y color verde en alternativas fallidas.
                                $(".input_fill").each(function (index) {                                // bloquear todas las alternativas.
                                    $(this).css("color", "green").val(array_respuesta_correcta[index]);
                                    $(this).attr('disabled', true);
                                });

                            }

                            else if(parseInt($('#tipo_ejercicio').val())== 2){                         // tipo seleccion unica.

                                $('#ModalUltimoIntentoFallidoPreguntaAlternativas').modal('show');      // modal mensaje de ultimo intento fallido.

                                $('.input_radio').prop('checked', false);                               // desclick a todas las alternativas.

                                respuesta_correcta = convertirNumero(response.respuesta_correcta);      // bloquear solo las alternativas incorrectas.

                                $(".input_radio").each(function (index) {
                                    if(parseInt($(this).val()) != respuesta_correcta) {
                                         $(this).attr('disabled', true);
                                    }
                                });

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
                            }

                        }
                     }

                }else if (parseInt(response.estatus)==0){
                     console.log(response.mensaje)
                     // mostrar modal amigable de error.
                }

            }

        });



}

function convertirLetra(numero){

  switch(numero)
  {
    case 1: return "A";
    case 2: return "B";
    case 3: return "C";
    case 4: return "D";
    case 5: return "E";
    case 6: return "F";
    case 7: return "G";
    case 8: return "H";
    case 9: return "I";
    case 10: return "J";
    case 11: return "K";
    case 12: return "L";
    case 13: return "M";
    case 14: return "N";
    case 15: return "O";
    case 16: return "P";
    case 17: return "Q";
    case 18: return "R";
    case 19: return "S";
    case 20: return "T";
    case 21: return "U";
    case 22: return "V";
    case 23: return "W";
    case 24: return "X";
    case 25: return "Y";
    case 26: return "Z";
  }

  return "numero no definido";
}

function convertirNumero(letra){

  switch(letra)
  {
    case "A": return 1;
    case "B": return 2;
    case "C": return 3;
    case "D": return 4;
    case "E": return 5;
    case "F": return 6;
    case "G": return 7;
    case "H": return 8;
    case "I": return 9;
    case "J": return 10;
    case "K": return 11;
    case "L": return 12;
    case "M": return 13;
    case "N": return 14;
    case "O": return 15;
    case "P": return 16;
    case "Q": return 17;
    case "R": return 18;
    case "S": return 19;
    case "T": return 20;
    case "U": return 21;
    case "V": return 22;
    case "W": return 23;
    case "X": return 24;
    case "Y": return 25;
    case "Z": return 26;
  }

  return "numero no definido";
}

function detenerAudioEjercicio(){

   // si el audio del ejercicio esta escuchandose, entonces lo detengo.
    if($('#audioEjercicio')[0].currentTime > 0 && !($('#audioEjercicio')[0].ended)){
        $('#audioEjercicio')[0].autoplay = false;
        $('#audioEjercicio')[0].load();
    }

}

function mostrarSolucionEjercicio(){

     $("#imagen_ejercicio").attr("src", "data:;base64,"+imagenSolucion);
     $("#div_input").html('');                                                      // quitar las las alternativas del ejercicio (input)
     $("#div_parlanteEjercicio").hide();
     $("#div_parlanteSolucionEjercicio").show();
     $("#div_botonAvanzarEjercicio").hide();
     $("#div_botonAvanzarSolucionEjercicio").show();

     if(parseInt($("#numero_nivel").val())== 3 || parseInt($("#numero_nivel").val())== 4){
        $("#src_ogg_solucion_ejercicio").attr("src", static_url+"core/audios/materiales/"+$("#nombre_actividad").val().toLowerCase()+"_e"+$("#npregunta").val()+"_pop.ogg");
        $("#src_mp3_solucion_ejercicio").attr("src", static_url+"core/audios/materiales/"+$("#nombre_actividad").val().toLowerCase()+"_e"+$("#npregunta").val()+"_pop.mp3");
        $('#audioSolucionEjercicio')[0].load();
        $('#audioSolucionEjercicio')[0].play();
     }

}