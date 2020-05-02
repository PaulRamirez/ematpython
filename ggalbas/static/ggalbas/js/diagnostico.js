
$(window).on('load', function (e) {
    $(".carga").fadeOut("slow");
});


$( document ).ready(function() {

    $('#vuelveAnteP').on('click', function(){
        $(location).attr('href','antePortada');
    });

    $('#numeroEjercicio').tooltip();

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

    $('#parlanteEjercicio').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
         $('#audioEjercicio')[0].load();
         $('#audioEjercicio')[0].play();
    });


    $('#ModalPreguntaSinContestar').on('shown.bs.modal', function () {

        detenerAudioEjercicio();
        $('#audioSinRespuesta')[0].load();
        $('#audioSinRespuesta')[0].play();
    });

    $('#ModalPreguntaSinContestar').on('hidden.bs.modal', function (e) {
        $('#audioSinRespuesta')[0].load();
    });

    $('#botonAvanzarEjercicio').on('click', function(e){
       e.preventDefault();
       e.stopImmediatePropagation();

       $(this).addClass('disabled');

       proximoEjercicio();
    });

    $('#botonAceptar').on('click', function(e){
       guardaRespuesta();
    });

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

    if(isMobile.any()){
        $('.fill-input').focus(function() {
          fillFocus = this;
          this.blur();
        });
    }

});

function proximoEjercicio(){



    var preguntaSinContestar=false;

    if ($('.input_fill').length) { // tipo fill

        $(".input_fill").each(function (index) {
            if($(this).val().trim()==''){
                preguntaSinContestar = true;  // el alumno no responde a una opcion.
                return false;
            }
        });

    }

    else if ($('.input_radio').length) {                         // tipo seleccion unica

          if (parseInt($('.input_radio:checked').length) < 1 ){
                preguntaSinContestar = true;
            }
    }

    else if($('.input_checkbox').length){

       if (parseInt($('.input_checkbox:checked').length) < 1 ){
                preguntaSinContestar = true;
            }
    }

       if(preguntaSinContestar==true){

            $('#ModalPreguntaSinContestar').modal('show');
            $( "#botonAvanzarEjercicio").removeClass('disabled');
        }else{
            guardaRespuesta();
        }

}

function guardaRespuesta(){



        respuestaAlumno = '';

        if($('.input_fill').length) {          // si el ejercicio es de tipo fill.

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

        else if($('.input_radio').length){

             if (parseInt($('.input_radio:checked').length) < 1 ){
                    respuestaAlumno = ''
             }else{
                respuestaAlumno = $("input[name='inputRadio']:checked").val();
             }

        }

        else if ($('.input_checkbox').length) {

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
                url: "guardaRespuesta",
                dataType: 'json',
                data: { 'respuestaAlumno': respuestaAlumno },
                success:function(respuesta){

                    if (respuesta.fin){
                        $(location).attr('href','portadaFinalDiagnostico');
                    }
                    else if (respuesta.alumnoRespuesta){
                         $(location).attr('href','visorActividades');
                    } else{
                        console.log ('aqui va el modal de error');
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
