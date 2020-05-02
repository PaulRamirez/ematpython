$( document ).ready(function() {

    validarActividadComplementariaIniciada();

    $('.botonVerActividad').on('click', function(e){

        e.preventDefault();
        e.stopImmediatePropagation();

        //limpiarModal();

        // datos de la actividad
        $('#id_alumno_actividad').val(0);
        $('#id_contenido_fase_actividad').val($(this).data('idcontenidofaseact'));
        $('#intento').val($(this).data('intento'));

        $('#nombreContenido').val($(this).data('contenido'));
        $('#nombreTipoAct').val($(this).data('tipoact'));
        $('#siglasAct').val($(this).data('siglas'));
        $('#ultimoPuntaje').val($(this).data('puntaje'));
        $('#fechaUltimoPuntaje').val($(this).data('fecha'));

        $.ajax({
                async: true,
                type: "POST",
                url: "validarUnidadSigHabilitada",
                dataType: 'json',
                data: {'ordenUnidadActual': $('li.unidadActiva').find('a').attr('id') },
                success:function(data){

                    if(parseInt(data.estatus)==1){

                        if(parseInt(data.opcionActivarUnidades)==0){
                            $('#modalRegresarLibroAlumno').modal('show');// abrir modal 1
                        }

                        else if(parseInt(data.opcionActivarUnidades)==1 && parseInt(data.total_contenidos) == parseInt(data.total_contenidos_activos)){
                            $('#modalRegresarLibroAlumno').modal('show');// abrir modal 1
                        }

                        else if(parseInt(data.autonomo)==1){
                            $('#modalRegresarLibroAlumno').modal('show');// abrir modal 1
                        }

                        else if(parseInt(data.opcionActivarUnidades)==1 && parseInt(data.total_contenidos_activos) < parseInt(data.total_contenidos)){

                            $('#modalFormInformativoActividad').modal('show');// abrir el modal.
                            $('#botonVolverMenu').show();   //mostrar boton
                            $('#botonSalirMenu').hide();    //ocultar boton
                            $('#tituloModalFormInformativoActividad').html('Actividad seleccionada:');
                        }
                    }
                }
        });


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

    $('#modalRegresarLibroAlumno').on('hidden.bs.modal', function (e) {
      $(location).attr('href','unidadesAlumno');
    })

     // modal de instrucciones.
     $('.btn-instrucciones').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $('#modalInstruccionesComplUnidad').modal('show');
     });

    $('#modalFormInformativoActividad').on('hidden.bs.modal', function (e) {
           limpiarModal();
    })

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

                     if (parseInt(data.id_alumno_actividad) !=0 ){

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

                     }else{

                             $.ajax({
                                async: true,
                                type: "POST",
                                url: "validarUnidadSigHabilitada",
                                dataType: 'json',
                                data: {'ordenUnidadActual': $('li.unidadActiva').find('a').attr('id') },
                                success:function(data){
                                    if(parseInt(data.estatus)==1){

                                        if(parseInt(data.opcionActivarUnidades)==0){
                                            $('#modalRegresarLibroAlumno').modal('show');// abrir modal 1
                                        }

                                        else if(parseInt(data.opcionActivarUnidades)==1 && parseInt(data.total_contenidos) == parseInt(data.total_contenidos_activos)){
                                            $('#modalRegresarLibroAlumno').modal('show');// abrir modal 1
                                        }

                                        else if(parseInt(data.autonomo)==1){
                                            $('#modalRegresarLibroAlumno').modal('show');// abrir modal 1
                                        }

                                    }
                                }
                            });
                        }



                }
            }
        });

}
