var url;
var respuestaAlumno;

$( document ).ready(function() {

    $('#continuar').on('click', function(){
        $(location).attr('href','portadaVisor');
    });

    $('#vuelveAnteP').on('click', function(){
        $(location).attr('href','antePortada');
    });

    $('#botonSalir').on('click', function(){
        $(location).attr('href','/ggalbas/');
    });

    $('#numeroEjercicio').tooltip();

    var fillFocus = $('.fill-input').first();

    $('.fill-input').on('click', function(){
       fillFocus = $(this);
    });

    $('.tecladoVirtual').on('click', function(){
        var simbolo = $(this).text().trim();
        fillFocus.val($.trim(fillFocus.val()) + simbolo);
    });

    $('#botonBorrar').on('click', function(){
      fillFocus.val($.trim(fillFocus.val()).slice(0, -1));
    });

    if ($('#player').length) {

        var player = $('#player');
        player[0].muted=false;

        $('#botonRepetir').on('click', function(e){
            e.preventDefault();
            e.stopImmediatePropagation();
             player[0].load();
             player[0].play();
        });
    }

      if ($('#audioSinRespuesta').length) {

            var audioSinRespuesta = $('#audioSinRespuesta');

            $('#ModalConfirmacion').on('shown.bs.modal', function () {
                    if(player[0].autoplay){
                          player[0].autoplay = false;
                    }
                    if(player[0].currentTime > 0 && !(player[0].ended)){
                          player[0].load();
                    }

                    audioSinRespuesta[0].load();
                    var prom = audioSinRespuesta[0].play();
                      if (prom !== undefined) {
                        prom.then(_ => {
                             console.log('exito play audioSinRespuesta');
                        })
                        .catch(error => {
                              console.log('error 2: '+error);
                        });
                      }else{
                       console.log('error 3');
                      }
            });

            $('#ModalConfirmacion').on('hidden.bs.modal', function (e) {
                audioSinRespuesta[0].load();
            });
       }

        $('#botonAvanzar').on('click', function(e){
           e.preventDefault();
           e.stopImmediatePropagation();
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

        var abecedario=new Array('A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z');

        var continuar=1;

        var valor = '';

        respuestaAlumno = '';

        if ($('.fill-input').length) { // los campos son de tipo text
            $(".fill-input").each(function (index) {
                if($(this).val().trim()==''){
                    valor= 'null';
                    continuar = 0;
                }else{
                    valor = $(this).val().trim().replace(",", ".");
                }
                respuestaAlumno += respuestaAlumno == '' ? String(valor) : ","+String(valor);
            });
        }


        if ($('.radio-check').length) { // los campos son de tipo radio o de tipo checkbox.
            $(".radio-check").each(function (index) {
                if($(this).is(':checked')) {
                    respuestaAlumno += abecedario[parseInt($(this).attr('id')) -1];
                }          
            });

            if(respuestaAlumno == ''){
                continuar = 0;
            }
        }

          if(continuar==0){
                $('#ModalConfirmacion').modal('show');
            }else{
                guardaRespuesta();
            }

}

function guardaRespuesta(){
            $('#botonAvanzar').fadeOut('fast');
            $.ajax({
                async: true,
                type: "POST",
                url: "guardaRespuesta",
                dataType: 'json',
                data: { 'respuestaAlumno': respuestaAlumno },
                success:function(respuesta){
                $('#botonAvanzar').fadeIn('fast');
                    if (respuesta.fin){
                        $(location).attr('href','resultadoDiagnostico');
                    }
                    else if (respuesta.alumnoRespuesta){
                         $(location).attr('href','visorActividades');
                    } else{
                        console.log ('aqui va el modal de error');
                    }
                }
            });
}
