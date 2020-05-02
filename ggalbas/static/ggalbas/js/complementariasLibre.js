$( document ).ready(function() {

   validarActividadComplementariaIniciada();

    $('.botonVerActividad').on('click', function(e){

        e.preventDefault();
        e.stopImmediatePropagation();

        // datos de la actividad
        $('#id_alumno_actividad').val(0);
        $('#id_contenido_fase_actividad').val($(this).data('idcontenidofaseact'));
        $('#intento').val($(this).data('intento'));

        $('#nombreContenido').val($(this).data('contenido'));
        $('#nombreTipoAct').val($(this).data('tipoact'));
        $('#siglasAct').val($(this).data('siglas'));
        $('#ultimoPuntaje').val($(this).data('puntaje'));
        $('#fechaUltimoPuntaje').val($(this).data('fecha'));

        $('#modalFormInformativoActividad').modal('show');// abrir el modal.
        $('#botonVolverMenu').show();   //mostrar boton
        $('#botonSalirMenu').hide();    //ocultar boton
        $('#tituloModalFormInformativoActividad').html('Actividad seleccionada:');


    });

     $('#botonIniciarActividadComp').on('click', function(e){

        var ultimasSiglasActividad = $('#siglasAct').val().substr($('#siglasAct').val().length - 2);

         if(parseInt($('#id_alumno_actividad').val()) == 0){ // inicia una nueva actividad complementaria

              $('#botonIniciarActividadComp').prop("disabled", true);

                var formData = new FormData($("#formIniciarActividad")[0]);

                $.ajax({
                    type: "POST",
                    url: "iniciarActividadComp",
                    processData: false,
                    contentType: false,
                    dataType: "json",
                    data: formData,
                    success:function(data){

                          $('#botonIniciarActividadComp').prop("disabled", false);

                          $('#modalFormInformativoActividad').modal('hide');

                          if(ultimasSiglasActividad == 'A1' || ultimasSiglasActividad == 'A2' || ultimasSiglasActividad == 'B2' || ultimasSiglasActividad == 'D2' || ultimasSiglasActividad == 'E2' || ultimasSiglasActividad == 'D1' || ultimasSiglasActividad == 'P1' || ultimasSiglasActividad == 'R1' || ultimasSiglasActividad == 'P2' || ultimasSiglasActividad == 'R2' || ultimasSiglasActividad == 'Q2' || ultimasSiglasActividad == 'S2'){
                            $(location).attr('href','/visores/portadaInicialAprendizaje');
                          }

                          if(ultimasSiglasActividad == 'A4' || ultimasSiglasActividad == 'Z1' || ultimasSiglasActividad == 'Z2' || ultimasSiglasActividad == 'Z4' || ultimasSiglasActividad == 'Z5' || ultimasSiglasActividad == 'Z6' || ultimasSiglasActividad == 'Z7' || ultimasSiglasActividad == 'Z8' || ultimasSiglasActividad == 'Z9' || ultimasSiglasActividad == 'Z0'){
                            $(location).attr('href','/visores/visorIntegracion');
                          }

                    }

                 });

         }else{

                $('#modalFormInformativoActividad').modal('hide');  // cerrar el modal.

                if(ultimasSiglasActividad == 'A1' || ultimasSiglasActividad == 'A2' || ultimasSiglasActividad == 'B2' || ultimasSiglasActividad == 'D2' || ultimasSiglasActividad == 'E2' || ultimasSiglasActividad == 'D1' || ultimasSiglasActividad == 'P1' || ultimasSiglasActividad == 'R1' || ultimasSiglasActividad == 'P2' || ultimasSiglasActividad == 'R2' || ultimasSiglasActividad == 'Q2' || ultimasSiglasActividad == 'S2'){
                    $(location).attr('href','/visores/portadaInicialAprendizaje');
                }

                if(ultimasSiglasActividad == 'A4' || ultimasSiglasActividad == 'Z1' || ultimasSiglasActividad == 'Z2' || ultimasSiglasActividad == 'Z4' || ultimasSiglasActividad == 'Z5' || ultimasSiglasActividad == 'Z6' || ultimasSiglasActividad == 'Z7' || ultimasSiglasActividad == 'Z8' || ultimasSiglasActividad == 'Z9' || ultimasSiglasActividad == 'Z0'){
                    $(location).attr('href','/visores/visorIntegracion');
                }
         }
    });

    /*funcion que limpia el modal informativo de la actividad seleccionada.*/
    $('#modalIniciarActividad').on('hidden.bs.modal', function (e) {
         limpiarModal();
    })

    $('ul.container-unidades li').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $(this).closest('ul').find('li').removeClass('unidadActiva disabled').addClass('completed');
        $(this).addClass('unidadActiva disabled').removeClass('completed');
        $('.bloqueUnidades').hide();    // ocultar todas las unidades.
        $('#bloqueUnidad_'+$(this).attr("id")).show();  //mostrar la unidad seleccionada.
        $('body') .css('background-image', 'url(/static/core/images/fondos/bgUnidad' + $(this).attr("id").toString() + '.png )' ); // cambia la imagen de fondo de acuerdo a unidad.
    });

    $('ul.container-unidades li').first().trigger( "click" ); // por defecto la primer unidad esta seleccionada.

     $('.btn-instrucciones').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $('#modalInstruccionesComplLibre').modal('show');
     });
         
});

function limpiarModal(){
      $('#id_alumno_actividad').val(0);
      $('#id_contenido_fase_actividad').val('');
      $('#intento').val('');
      $('#nombreContenido').val('');
      $('#nombreTipoAct').val('');
      $('#siglasAct').val('');
      $('#ultimoPuntaje').val('');
      $('#fechaUltimoPuntaje').val('');
}


function validarActividadComplementariaIniciada(){

      $.ajax({
            async: true,
            type: "POST",
            url: "validarActividadComplementariaIniciada",
            dataType: 'json',
            success:function(data){

                if (parseInt(data.estatus)==1){

                     if (parseInt(data.id_alumno_actividad) !=0){

                            // datos de la actividad
                            $('#id_alumno_actividad').val(data.id_alumno_actividad);
                            $('#id_contenido_fase_actividad').val(data.id_contenido_fase_actividad);
                            $('#intento').val(data.intento);

                            $('#nombreContenido').val(data.nombreContenido);
                            $('#nombreTipoAct').val(data.nombreTipoAct);
                            $('#siglasAct').val(data.siglasAct);
                            $('#ultimoPuntaje').val(data.ultimoPuntaje);
                            $('#fechaUltimoPuntaje').val(data.fechaUltimoPuntaje);
                            // abrir el modal.
                            $('#modalFormInformativoActividad').modal({backdrop: 'static', keyboard: false}) ;
                            $('#tituloModalFormInformativoActividad').html('Actividad en Curso:');
                            $('#botonVolverMenu').hide();
                            $('#botonSalirMenu').show();

                     }
                }
            }
        });

}