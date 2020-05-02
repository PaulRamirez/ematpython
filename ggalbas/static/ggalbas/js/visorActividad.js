$( document ).ready(function() {

      $('a.volver').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();
        validarContenidoTerminado();
       });

});

function validarContenidoTerminado(){
    $.ajax({
        async: true,
        type: "POST",
        url: "validarContenidoTerminado",
        dataType: 'json',
        success:function(data){

            if(parseInt(data.estatus)==1){  // si no tiene mas actividades en el contenido.
                $(location).attr('href','unidadesAlumno');
            }else if(parseInt(data.estatus)==2){    // si aun tiene actividades en el contenido.
                $(location).attr('href','contenidosAlumno');
            }else if(parseInt(data.estatus)==0){
                console.log(data.mensaje);
            }
        }
    });
}