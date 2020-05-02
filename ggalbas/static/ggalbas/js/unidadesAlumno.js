$( document ).ready(function() {

   var autonomo = parseInt($("#autonomo").data( "autonomo" ));

   total_unidades = parseInt($('ul.container-unidades li').length);

   orderUnidadActual =  parseInt($('ul.container-unidades li.actual').attr('id'));

   ordenUnidadSiguiente = orderUnidadActual + 1 ;

   total_contenidos = parseInt($('#bloqueContenido_'+orderUnidadActual).find('ul.list-desglose-contenido li').length);

   total_completados = parseInt($('#bloqueContenido_'+orderUnidadActual).find('ul.list-desglose-contenido li').find('a.completed').length);


    if((total_contenidos == total_completados) && (orderUnidadActual == total_unidades)){
         $(location).attr('href','complementariasLibre');
     }

    if((total_contenidos == total_completados) && (orderUnidadActual < total_unidades) && autonomo==0){

            setTimeout(function(){
                validarUnidadSigHabilitada();
            }, 1000);
    }

    if((total_contenidos == total_completados) && (orderUnidadActual < total_unidades) && autonomo==1){
            setTimeout(function(){
                $('#modalContinuarViaje').modal('show');
            }, 1000);

    }

    $('#modalComplementarias').on('hidden.bs.modal', function (e) { // evento al cerrar el modal 2
      $(location).attr('href','complementariasUnidad');
    });

   // evento al cerrar el modal 1
    $('#modalContinuarViaje').on('hidden.bs.modal', function (e) {
          $('ul.container-unidades li').filter('#'+orderUnidadActual).removeClass('actual').addClass('completed');
          $('ul.container-unidades li').filter('#'+ordenUnidadSiguiente).addClass('actual');
          $('.bloqueContenidos').hide();
          $('#bloqueContenido_'+ordenUnidadSiguiente).show();
          $('body') .css('background-image', 'url(/static/core/images/fondos/bgUnidad' + ordenUnidadSiguiente.toString() + '.png )' );
    });



    $('ul.list-desglose-contenido li').find('a.actual').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        $(location).attr('href','contenidosAlumno');
    });

});

function validarUnidadSigHabilitada(){

    $.ajax({
            async: true,
            type: "POST",
            url: "validarUnidadSigHabilitada",
            dataType: 'json',
            data: { 'ordenUnidadActual': $('ul.container-unidades li.actual').attr('id')  },
            success:function(data){

                if(parseInt(data.estatus)==1){

                    if(parseInt(data.opcionActivarUnidades)==0){
                        $('#modalContinuarViaje').modal('show');// abrir modal 1
                    }

                    if(parseInt(data.opcionActivarUnidades)==1 && parseInt(data.total_contenidos)== parseInt(data.total_contenidos_activos)){
                        $('#modalContinuarViaje').modal('show');// abrir modal 1
                    }
                    if(parseInt(data.opcionActivarUnidades)==1 && parseInt(data.total_contenidos_activos) < parseInt(data.total_contenidos)){
                        $('#modalComplementarias').modal('show');  // abrir modal 2
                    }

                }
            }
     });

}