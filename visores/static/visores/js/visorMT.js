$(window).on('load', function (e) {
    $(".carga").fadeOut("slow");
});

$( document ).ready(function() {

    $('#numeroEjercicio').tooltip();

    $('#botonVolverPortadaInicialMT').on('click', function(){
        $(location).attr('href','/ggalbas/contenidosAlumno');
    });

    $('#botonAvanzarEjercicio').on('click', function(e){

        e.preventDefault();
        e.stopImmediatePropagation();

        $( "#botonAvanzarEjercicio").addClass('disabled');

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
                $('#ModalPreguntaSinResponder').modal('show');
                $( "#botonAvanzarEjercicio").removeClass('disabled');
            }else{
                guardaRespuestaMT();
            }
    });

    $('#botonAceptarModal').on('click', function(e){
       guardaRespuestaMT();
    });

    //teclado virtual.
    var fillFocus = $('.fill-input').first(); // posiciono el foco en el primer elemento de tipo fill (completar).

    $('.fill-input').on('click', function(){
       fillFocus = $(this);
    });

    $('.tecladoVirtual').on('click', function(){    // usando el teclado virtual.
        var simbolo = $(this).text().trim();
        fillFocus.val($.trim(fillFocus.val()) + simbolo);
    });

    $('#botonBorrar').on('click', function(){
      fillFocus.val($.trim(fillFocus.val()).slice(0, -1));
    });

    //detectar si la aplicacion esta abierta en dispositivo movil.
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
        $('.fill-input').focus(function() {
          fillFocus = this;
          this.blur();
        });
    }

    $('#parlanteEjercicio').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
         $('#audioEjercicio')[0].load();
         $('#audioEjercicio')[0].play();
    });


    $('#ModalPreguntaSinResponder').on('shown.bs.modal', function () {
        detenerAudioEjercicio();
        $('#audioPreguntaSinResponder')[0].load();
        $('#audioPreguntaSinResponder')[0].play();
    });

    $('#ModalPreguntaSinResponder').on('hidden.bs.modal', function (e) {
        $('#audioPreguntaSinResponder')[0].load();
    });


});

function guardaRespuestaMT(){

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

    $.ajax({
        async: true,
        type: "POST",
        url: "guardaRespuestaMT",
        dataType: 'json',
        data: {
                'id_alumno_actividad': $('#id_alumno_actividad').val(),
                'npregunta': $('#npregunta').val(),
                'tipo_ejercicio': $('#tipo_ejercicio').val(),
                'num_campos_completar': $('#num_campos_completar').val(),
                'respuestaAlumno': respuestaAlumno
              },
        success:function(response){

            if(parseInt(response.estatus)==1) // se guarda correctamente la respuesta, avanza a la siguiente pregunta.
            {
                $(location).attr('href','visorMT');
            }
            else{
                console.log(response.mensaje)
            }
        }

        });
}

function detenerAudioEjercicio(){
    if($('#audioEjercicio')[0].currentTime > 0 && !($('#audioEjercicio')[0].ended)){
          $('#audioEjercicio')[0].autoplay = false;
          $('#audioEjercicio')[0].load();
    }
}