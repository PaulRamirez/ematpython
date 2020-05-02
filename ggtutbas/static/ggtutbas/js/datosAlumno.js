var tablaAlumno;
var pais= $('#pais').val().trim();

$( document ).ready(function() {

tablaAlumno=$('#tablaAlumno').dataTable({
		"aProcessing":true,
		"aServerSide": true,
		"searching": true,
		"paging": false,
		"language": {
            "info": "mostrando del _START_ al _END_ de un total de _TOTAL_ registros",
            "search": "Buscar:"
          },
		"bDestroy": true,
		"ajax":{
			url:'/ggtutbas/listarAlumnosPorLista',
			type:"POST",
			dataType:"json",
			error: function(e){
				console.log(e.responseText);
			}
		},
	}).DataTable();


    $.post("/ggtutbas/listarPreguntaUsuarios", function(r){
             $("#id_pregunta").html(r);
    });

    $('#ModalNuevoAlumno').on('hidden.bs.modal', function (e) {
        limpiarFormNuevoAlumno();
        limpiarMensajeErrorNuevoAlumno();
    })



    $("#id_producto").click( function(){
       if( $(this).is(':checked') ){
         $("#autonomo").prop("checked", false);
         $("#autonomo").attr("disabled", true);
       }else{
         $("#autonomo").attr("disabled", false);
       }
    });


    $("#autonomo").click( function(){
       if( $(this).is(':checked') ) {
        $("#id_producto").prop("checked", false);
        $("#id_producto").attr("disabled", true);
       }else{
        $("#id_producto").attr("disabled", false);
       }
    });



    $('#botonAgregarAlumno').on('click', function(e){

        limpiarMensajeErrorNuevoAlumno();

        if($('#rut').val().trim()==''){
            $('#rut').focus();
            if (pais=='cl'){
                $('#errorRutRegistrar').html('Para registrarse ingrese su RUT');
            }
            else{
                $('#errorRutRegistrar').html('Para registrarse ingrese su Id usuario');
                }
        }else if($('#validador').val().trim()==''){
            $('#validador').focus();
            if (pais=='cl'){
                $('#errorRutRegistrar').html('Para registrarse ingrese su RUT');
             }
             else{
                $('#errorRutRegistrar').html('Para registrarse ingrese su Id usuario');
             }
        }else if (Fn.validaRut($('#rut').val()+'-'+$('#validador').val())==false){
            $('#rut').focus();
            if (pais=='cl'){
            $('#errorRutRegistrar').html('Debe ingresar un Rut válido');
            }
            else{
                $('#errorRutRegistrar').html('Debe ingresar un Id usuario válido');
            }
        }else if($('#nombre').val().trim()==''){
            $('#nombre').focus();
            $('#errorNombreRegistrar').html('Para registrarse ingrese sus nombres');
        }else if($('#nombre').val().trim().length < 2){
            $('#nombre').focus();
            $('#errorNombreRegistrar').html('Sus nombres debe tener mínimo 3 caracteres');
        }else if($('#apellido').val().trim()==''){
            $('#apellido').focus();
            $('#errorApellidoRegistrar').html('Para registrarse ingrese sus apellidos');
        }else if($('#apellido').val().trim().length < 2){
            $('#apellido').focus();
            $('#errorApellidoRegistrar').html('Sus apellidos debe tener mínimo 3 caracteres');
        }else if($('#id_pregunta').val()==""){
           $('#id_pregunta').focus();
           $('#errorPreguntaRegistrar').html('Para registrarse seleccione una pregunta de seguridad');
        }else if($('#respuesta').val().trim()==""){
           $('#respuesta').focus();
           $('#errorRespuestaRegistrar').html('Para registrarse escriba la respuesta a la pregunta de seguridad');
        } else{

        $("#botonAgregarAlumno").prop("disabled", true);

        var formData = new FormData($("#formNuevoAlumno")[0]);

              $.ajax({
                  async: true,
                  type: "POST",
                  url: "/ggtutbas/guardarAlumno",
                  dataType: 'json',
                  data: formData ,
                  contentType: false,
		          processData:false,
                  success: function(data){
                    if (parseInt(data.estatus) == 0){
                        $('#errorRegistrarAlumno').html(data.mensaje);
                        $("#botonAgregarAlumno").prop("disabled", false);
                    }else{
                        $('#ModalNuevoAlumno').modal('hide');
                        $('#passwordNuevo').html(data.clave);
                        $('#ModalPassword').modal('show');
                        tablaAlumno.ajax.reload();
                        mostarMensaje('El alumno fue registrado con exito.');
                    }
                  },
                  error: function(e){
                    console.log('error: '+e)
                    $('#errorRegistrarAlumno').html(e);
                    $("#botonAgregarAlumno").prop("disabled", false);
                  }
                });
        }
    });

    $('#botonEditarAlumno').on('click', function(e){

        limpiarMensajeErrorEditarAlumno();

         if($('#nombreAlumno').val().trim()==''){
            $('#nombreAlumno').focus();
            $('#errorNombreEditar').html('Para registrarse ingrese sus nombres');
        }else if($('#nombreAlumno').val().trim().length < 3){
            $('#nombreAlumno').focus();
            $('#errorNombreEditar').html('Sus nombres debe tener mínimo 3 caracteres');
        }else if($('#apellidoAlumno').val().trim()==''){
            $('#apellidoAlumno').focus();
            $('#errorApellidoEditar').html('Para registrarse ingrese sus apellidos');
        }else if($('#apellidoAlumno').val().trim().length < 3){
            $('#apellidoAlumno').focus();
            $('#errorApellidoEditar').html('Sus apellidos debe tener mínimo 3 caracteres');
        } else{

            $("#botonEditarAlumno").prop("disabled", true);

            var formData = new FormData($("#formEditarAlumno")[0]);

              $.ajax({
                  async: true,
                  type: "POST",
                  url: "/ggtutbas/verificarAlumno",
                  dataType: 'json',
                  data: formData ,
                  contentType: false,
		          processData:false,
                  success: function(data){

                    $("#botonEditarAlumno").prop("disabled", false);
                    $("#botonConfirma").prop("disabled", true);

                    if (parseInt(data.estatus) == 0){ // error al validar.
                        $('#errorEditarAlumno').html(data.mensaje);
                    }else if(parseInt(data.estatus) == 1){ //sin modificar
                        editarAlumno();
                    }else if(parseInt(data.estatus) == 2){  //  Otorgado la modalidad de trabajo autonomo.
                         $('#textoTerminoCondiciones').html('Le has otorgado al alumno '+$('#nombreAlumno').val() +' ' + $('#apellidoAlumno').val() + ' , la modalidad de trabajo <strong>autónomo.</strong> ¿Estas seguro de esta decisión?')
                         $('#ModalEditarAlumno').modal('hide');
                         $('#ModalConfirma').modal('show');
                    }else if(parseInt(data.estatus) == 3){ // Otorgado el plan de trabajo diferenciado.
                        $('#textoTerminoCondiciones').html('Le has otorgado al alumno '+$('#nombreAlumno').val() +' ' +$('#apellidoAlumno').val() + ' , el <strong>plan de trabajo diferenciado.</strong> ¿Estas seguro de esta decisión?')
                        $('#ModalEditarAlumno').modal('hide');
                        $('#ModalConfirma').modal('show');
                    }
                    else if(parseInt(data.estatus) == 4){ // Otorgado el plan de trabajo diferenciado.
                        $('#textoTerminoCondiciones').html('Le has removido al alumno '+$('#nombreAlumno').val() +' ' +$('#apellidoAlumno').val() + ' , el <strong>plan de trabajo diferenciado.</strong> ¿Estas seguro de esta decisión?')
                        $('#ModalEditarAlumno').modal('hide');
                        $('#ModalConfirma').modal('show');
                    }
                  },
                  error: function(e){
                    console.log('error: '+e)
                    $('#errorEditarAlumno').html(e);
                    $("#botonEditarAlumno").prop("disabled", false);
                  }
                });
        }
    });

   $('#botonConfirma').on('click', function(e){
             editarAlumno();
   });

   $('.botonCancelar').on('click', function(e){
     $('#ModalConfirma').modal('hide');
     $('#ModalEditarAlumno').modal('show');
   });

    $("#aceptaCondiciones").click( function(){
       if( $(this).is(':checked') ){
         $("#botonConfirma").prop("disabled", false);
       }else{
         $("#botonConfirma").prop("disabled", true);
       }
    });

});

 var Fn = {
      // Valida el rut con su cadena completa "XXXXXXXX-X"
      validaRut : function (rutCompleto) {
        rutCompleto = rutCompleto.replace("‐","-");
        if (!/^[0-9]+[-|‐]{1}[0-9kK]{1}$/.test( rutCompleto ))
          return false;
        var tmp   = rutCompleto.split('-');
        var digv  = tmp[1];
        var rut   = tmp[0];
        if ( digv == 'K' ) digv = 'k' ;
        return (Fn.dv(rut) == digv );
      },
      dv : function(T){
        var M=0,S=1;
        for(;T;T=Math.floor(T/10))
          S=(S+T%10*(9-M++%6))%11;
        return S?S-1:'k';
      }
}

function consultarAlumno(rut_alumno,event){
    event.preventDefault();
    event.stopImmediatePropagation();

    limpiarFormEditarAlumno();
    limpiarMensajeErrorEditarAlumno();

	$.post("/ggtutbas/consultarAlumno", { 'rut': rut_alumno }, function(data){
		data = JSON.parse(data);
		$("#rutAlumno").val(data.rut_alumno);
        $("#nombreAlumno").val(data.nombre);
        $("#apellidoAlumno").val(data.apellido);
        if(data.id_producto==3){
            $("#id_producto").prop('checked', true);
            $("#autonomo").prop('disabled', true);
        }
        if(data.autonomo==1){
            $("#autonomo").prop('checked', true);
            $("#autonomo").prop('disabled', true);
            $("#id_producto").prop('disabled', true);
        }
         $('#ModalEditarAlumno').modal('show');

	});

}

function editarAlumno(){

    var formData = new FormData($("#formEditarAlumno")[0]);

      $.ajax({
          async: true,
          type: "POST",
          url: "/ggtutbas/editarAlumno",
          dataType: 'json',
          data: formData ,
          contentType: false,
          processData:false,
          success: function(data){
            if (parseInt(data.estatus) == 0){
                $("#botonConfirma").prop("disabled", false);
            }else{
                $('#ModalConfirma').modal('hide');
                $('#ModalEditarAlumno').modal('hide');
                tablaAlumno.ajax.reload();
                mostarMensaje('El alumno fue editado con exito.');
            }
          },
          error: function(e){
            console.log('error: '+e)
            $("#botonConfirma").prop("disabled", false);
          }
        });

}

function mostarMensaje(texto){
    $('#divMensaje').html(texto).fadeIn();
    setTimeout(function() {
        $('#divMensaje').fadeOut('slow');
    }, 1000);
}

function limpiarFormNuevoAlumno(){
  $("#botonAgregarAlumno").prop("disabled", false);
  $('#rut').val('');
  $('#validador').val('');
  $('#nombre').val('');
  $('#apellido').val('');
  $('#id_pregunta').val('');
  $('#respuesta').val('');
}

function limpiarMensajeErrorNuevoAlumno(){
    $('#errorRutRegistrar').html('');
    $('#errorNombreRegistrar').html('');
    $('#errorApellidoRegistrar').html('');
    $('#errorPreguntaRegistrar').html('');
    $('#errorRespuestaRegistrar').html('');
    $('#errorRegistrarAlumno').html('');
}

function limpiarFormEditarAlumno(){
  $("#botonEditarAlumno").prop("disabled", false);
  $('#rutAlumno').val('');
  $('#nombreAlumno').val('');
  $('#apellidoAlumno').val('');
  $("#id_producto").attr("disabled", false);
  $("#id_producto").prop('checked', false);
  $("#autonomo").attr("disabled", false);
  $("#autonomo").prop('checked', false);
  $("#aceptaCondiciones").prop('checked', false);
}

function limpiarMensajeErrorEditarAlumno(){
    $('#errorNombreEditar').html('');
    $('#errorApellidoEditar').html('');
    $('#errorEditarAlumno').html('');
}

function linkDesabilitado(e){
     e.preventDefault();
     e.stopImmediatePropagation();
}

function imprimirCredencial(){
$('#imprime-credencial').on('click', function(){
console.log('ping');
});
}
