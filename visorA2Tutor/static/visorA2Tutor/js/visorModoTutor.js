var imagenSolucion='';
var aprobada = 0;
var intento=0;
var maximo_intento;

$(window).on('load', function (e) {
    $(".carga").fadeOut("slow");

});

$( document ).ready(function() {

    maximo_intento = $("#maximo_intento").val();

    $('.numeroEjercicio').tooltip();

    $('#botonAvanzarEjercicio').on('click', function(e){

        e.preventDefault();
        e.stopImmediatePropagation();
        $( "#botonAvanzarEjercicio").addClass('disabled');

        var preguntaSinContestar = validarPreguntaSinResponder();

        if(preguntaSinContestar==true){
            // si no contesto la pregunta
            $('#ModalPreguntaObligatoria').modal('show');
            $( "#botonAvanzarEjercicio").removeClass('disabled');

        }else{

            if(intento < maximo_intento ){
                guardaRespuesta();
            }

            if(intento == maximo_intento){
               $(location).attr('href','ejercicios');
             }


        }

    });

    $('#botonAvanzarSolucionEjercicio').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        // inhabilita la botonera completamente.
        $("#botonAvanzarSolucionEjercicio").addClass('disabled');

        if(parseInt($('#npregunta').val()) < parseInt($('#total_ejercicios').val())){
            irPantallaEjercicio(parseInt($('#npregunta').val())+1);
        }else{
            terminoActividad();
        }

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

    $('#botonAnterior').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();

        // inhabilita la botonera completamente.
        $(".botones-desplazamiento").addClass('disabled');

        // si estoy en pantalla del primer ejercicio, entonces no puedo retroceder.
        if($("#divVisorEjercicio").is(":visible") && parseInt($('#npregunta').val()) == 1 ){
            $('#mensajeModalError').html('Ya est\u00E1 en el primer Ejercicio, no puede retroceder m\u00E1s');
            $('#modalError').modal('show');
            $(".botones-desplazamiento").removeClass('disabled');

        // si estoy en pantalla del pop entonces retrocedo al ejercicio actual.
        }else if($("#divSolucionEjercicio").is(":visible")){

            irPantallaEjercicio(parseInt($('#npregunta').val()));

        }else{

            // buscar el pop del ejercicio anterior.
            $.ajax({
                async: true,
                type: "POST",
                url: "buscarImagenSolucionEjercicio",
                dataType: 'json',
                data: {
                    'npregunta': parseInt($('#npregunta').val()) - 1,
                  },
                success:function(response){

                    // si estoy en pantalla de ejercicio y el ejercicio anterior tiene pop, entonces me dirijo a pop del ejercicio anterior.
                    if($("#divVisorEjercicio").is(":visible") && response.solucion_imagen != '' ){

                        irPantallaPop(parseInt($('#npregunta').val()) - 1 );
                    }
                    // si estoy en pantalla de ejercicio y el ejercicio anterior no tiene pop , entonces me dirijo a la pantalla del ejercicio anterior.
                    else if($("#divVisorEjercicio").is(":visible") && response.solucion_imagen == '' ){

                        irPantallaEjercicio(parseInt($('#npregunta').val()) - 1 );
                    }
                }
            });

        }

    });

    $('#botonIrEjercicio').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();

        // inhabilita la botonera completamente.
         $(".botones-desplazamiento").addClass('disabled');

        if($.trim($('#ir_ejercicio').val()) ==""){
            $('#mensajeModalError').html('Debe escribir el numero del ejercicio.');
            $('#modalError').modal('show');
            $(".botones-desplazamiento").removeClass('disabled');

        }else if(parseInt($.trim($('#ir_ejercicio').val())) < 1 || parseInt($.trim($('#ir_ejercicio').val())) > parseInt($('#total_ejercicios').val()) ){
            $('#mensajeModalError').html('El número de ejercicio escrito, no existe en esta actividad');
            $('#modalError').modal('show');
            $(".botones-desplazamiento").removeClass('disabled');

        }else{
                irPantallaEjercicio($.trim($('#ir_ejercicio').val()));
        }


    });

    $('#botonSiguiente').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();

        // inhabilita la botonera completamente.
        $( ".botones-desplazamiento").addClass('disabled');

        $.ajax({
            async: true,
            type: "POST",
            url: "buscarImagenSolucionEjercicio",
            dataType: 'json',
            data: {
                'npregunta': $('#npregunta').val(),
              },
            success:function(response){

                // si estoy en pantalla de un  ejercicio que no tiene pop, avanzo al siguiente ejercicio
                 if($("#divVisorEjercicio").is(":visible") && response.solucion_imagen == '' && parseInt($('#npregunta').val()) <  parseInt($('#total_ejercicios').val()) ){
                     irPantallaEjercicio(parseInt($('#npregunta').val())+1);
                 }

                // si estoy en pantalla del ejercicio y tiene pop, entonces muestro el pop.
                 else if($("#divVisorEjercicio").is(":visible") && response.solucion_imagen != ''){
                     irPantallaPop(parseInt($('#npregunta').val()));
                 }

                 // si estoy en pantalla del ultimo ejercicio y no tiene pop, entonces no puedo avanzar.
                 else if($("#divVisorEjercicio").is(":visible") && response.solucion_imagen == '' && parseInt($('#npregunta').val()) ==  parseInt($('#total_ejercicios').val()) ){
                     $('#mensajeModalError').html('Ya est\u00E1 en el \u00FAltimo Ejercicio, no puede avanzar  m\u00E1s.');
                     $('#modalError').modal('show');
                     $(".botones-desplazamiento").removeClass('disabled');
                 }

                 // si estoy en la pantalla de pop del ultimo ejercicio , entonces no puedo avanzar.
                 else if($("#divSolucionEjercicio").is(":visible") && parseInt($('#npregunta').val()) ==  parseInt($('#total_ejercicios').val()) ){
                     $('#mensajeModalError').html('Ya est\u00E1 en el \u00FAltimo Ejercicio, no puede avanzar  m\u00E1s.');
                     $('#modalError').modal('show');
                     $(".botones-desplazamiento").removeClass('disabled');
                 }

                 // si estoy en la pantalla del pop y no estoy en el ultimo ejercicio, entonces avanzo al siguiente ejercicio.
                 else if($("#divSolucionEjercicio").is(":visible") && parseInt($('#npregunta').val()) <  parseInt($('#total_ejercicios').val()) ){
                     irPantallaEjercicio(parseInt($('#npregunta').val())+1);
                 }

            }
        });

    });

    $("#ir_ejercicio").keydown(function(event) {

        // Desactivamos cualquier combinacion con shift
        if(event.shiftKey)
            event.preventDefault();

        // Solo Numeros del 0 a 9
        if (event.keyCode < 48 || event.keyCode > 57)
            //Solo Teclado Numerico 0 a 9
            if (event.keyCode < 96 || event.keyCode > 105)
                /*
                    No permite ingresar pulsaciones a menos que sean los siguientes
                    KeyCode Permitidos
                    keycode 8 Retroceso
                    keycode 37 Flecha Derecha
                    keycode 39  Flecha Izquierda
                    keycode 46 Suprimir
                */
                if(event.keyCode != 46 && event.keyCode != 8 && event.keyCode != 37 && event.keyCode != 39)
                    event.preventDefault();

    });

    $('#botonSalir').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();

        // inhabilita el boton cerrar.
        $("#botonSalir").addClass('disabled');

        $.ajax({
            async: true,
            type: "POST",
            url: "cerrarSesion",
            success:function(data){
                window.close();
               $("#botonSalir").removeClass('disabled');
            }
        });

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

function guardaRespuesta(){

    respuestaAlumno = obtenerRespuestaAlumno();

    $.ajax({
        async: true,
        type: "POST",
        url: "guardarPregunta",
        dataType: 'json',
        data: {
            'idguia': $('#idguia').val(),
            'total_ejercicios': $('#total_ejercicios').val(),
            'npregunta': $('#npregunta').val(),
            'tipo_ejercicio': $('#tipo_ejercicio').val(),
            'num_campos_completar': $('#num_campos_completar').val(),
            'maximo_intento': $('#maximo_intento').val(),
            'respuestaAlumno': respuestaAlumno
          },
        success:function(response){

            // si se guardo correctamente la respuesta
            if(parseInt(response.estatus)==1){

                aprobada = parseFloat(response.aprobada)      // set variables globales.
                intento = parseInt(response.intento)

                if(aprobada == 1 ){
                    $(location).attr('href','ejercicios');
                }

                // si respondio incorrecto y aun tiene intentos.
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

                // si respondio incorrecto y no tiene mas intentos
                if(aprobada < 1 && intento == maximo_intento){

                    imagenSolucion = response.solucion_imagen;

                    if(parseInt($('#tipo_ejercicio').val())== 1){                               // tipo fill.

                        $('#ModalUltimoIntentoFallidoPreguntaFill').modal('show');              // modal mensaje de ultimo intento fallido.

                        array_respuesta_correcta = response.respuesta_pregunta.split('~')

                        $(".input_fill").each(function (index) {
                            $(this).css("color", "green").val(array_respuesta_correcta[index]); // coloca la respuesta correcta en cada campo y con letra color verde.
                            $(this).attr('disabled', true);                                     // desabilita todos los campos
                        });

                        $( "#botonAvanzarEjercicio").removeClass('disabled');

                    }

                    else if(parseInt($('#tipo_ejercicio').val())== 2){                         // tipo seleccion unica.

                        $('#ModalUltimoIntentoFallidoPreguntaAlternativas').modal('show');      // modal mensaje de ultimo intento fallido.

                        $('.input_radio').prop('checked', false);                               // desclick a todas las alternativas.

                        respuesta_correcta = response.respuesta_pregunta;

                        $(".input_radio").each(function (index) {
                            if($(this).val() != respuesta_correcta) {
                                 $(this).attr('disabled', true);                                 // desabilita todas las alternativas menos la correcta
                            }                                                                    // los campos desabilitados se marcan con una X
                        });

                        $( "#botonAvanzarEjercicio").removeClass('disabled');

                    }

                    else if(parseInt($('#tipo_ejercicio').val())== 3){                         // tipo seleccion multiple.

                        $('#ModalUltimoIntentoFallidoPreguntaAlternativas').modal('show');     // modal mensaje de ultimo intento fallido.

                        $('.input_checkbox').prop('checked', false);                            // // desclick a todas las alternativas.

                        array_respuesta = response.respuesta_pregunta.split('~');
                        respuesta_incorrrecta = array_respuesta[1];
                        array_respuesta_incorrecta = respuesta_incorrrecta.split('');

                        $.each(array_respuesta_incorrecta, function (ind, elem) {
                            $('#checkbox-'+elem).attr('disabled', true);                    // desabilita todas las alternativas menos la(s) correcta(s)
                        });                                                                 // los campos desabilitados se marcan con una X

                        $( "#botonAvanzarEjercicio").removeClass('disabled');

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

function detenerAudioEjercicio(){

   // si el audio del ejercicio esta escuchandose, entonces lo detengo.
    if($('#audioEjercicio')[0].currentTime > 0 && !($('#audioEjercicio')[0].ended)){
        $('#audioEjercicio')[0].autoplay = false;
        $('#audioEjercicio')[0].load();
    }

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

function irPantallaEjercicio(npregunta){

    $.ajax({
        async: true,
        type: "POST",
        url: "irPantallaEjercicio",
        dataType: 'json',
        data: {
            'npregunta': npregunta,
          },
        success:function(response){
            $(location).attr('href','ejercicios');
        }
    });
}

function irPantallaPop(npregunta){

    $.ajax({
        async: true,
        type: "POST",
        url: "irPantallaPop",
        dataType: 'json',
        data: {
            'npregunta': npregunta,
          },
        success:function(response){
            $(location).attr('href','ejercicios');
        }
    });
}

function terminoActividad(){

    $.ajax({
        async: true,
        type: "POST",
        url: "terminoActividad",
        dataType: 'json',
        success:function(response){
            $(location).attr('href','ejercicios');
        }
    });
}