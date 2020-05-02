function isEmail(email) {
  var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  return regex.test(email);
}
  var url = jQuery(location).attr('href');

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

 validaForm();

 function validaForm(){
 $('#registro').on('click', function(){
 var pais= $('#pais').val().trim();
      if ($('#rut').val() =="" || $('#validador').val()==""){
            if (pais=='cl'){
            $('#textoErrorModal').html('Para registrarse ingrese su RUT');
            }
            else{
            $('#textoErrorModal').html('Para registrarse ingrese su Id usuario');
            }
            $('#modalError').modal("show");
       }
       else if (Fn.validaRut($('#rut').val()+'-'+$('#validador').val())==false){
          if (pais=='cl'){
            $('#textoErrorModal').html('El rut ingresado no es válido');
          }
          else{
          $('#textoErrorModal').html('El Id usuario ingresado no es válido');
          }
          $('#modalError').modal("show");
       }
       else if ($('#codColegio').val().trim()==""){
          $('#textoErrorModal').html('Para registrarse ingrese el código colegio (RBD)');
          $('#modalError').modal("show");
       }
       else if ($('#codUsuario').val().trim()==""){
          $('#textoErrorModal').html('Para registrarse ingrese el código usuario');
          $('#modalError').modal("show");
       }
       else if ($('#email').val().trim()==""){
          $('#textoErrorModal').html('Para registrarse ingrese su e-mail');
          $('#modalError').modal("show");
       }
       else if (isEmail($('#email').val())==false){
          $('#textoErrorModal').html('El e-mail ingresado no es válido');
          $('#modalError').modal("show");
       }
       else if (isEmail($('#email').val())==false){
          $('#textoErrorModal').html('El e-mail ingresado no es válido');
          $('#modalError').modal("show");
       }
       else if($('#TutorNombres').val().trim()=="" || $("#TutorNombres").val().trim().length < 2 ){
           $('#textoErrorModal').html('Para registrarse ingrese sus nombres, mínimo de 3 caracteres');
           $('#modalError').modal("show");
       }
       else if($('#TutorApellidos').val().trim()=="" || $("#TutorApellidos").val().trim().length < 2 ){
           $('#textoErrorModal').html('Para registrarse ingrese sus apellidos, mínimo 3 caracteres');
           $('#modalError').modal("show");
       }
       else if($('#TutorPassword').val().trim()=="" || $('#TutorPasswordRep').val().trim()==""){
           $('#textoErrorModal').html('Para registrarse ingrese un password');
           $('#modalError').modal("show");
       }
       else if($('#TutorPassword').val().trim().length < 6  || $('#TutorPasswordRep').val().trim().length < 6 ){
           $('#textoErrorModal').html('Para registrarse el password debe ser igual o mayor a 6 caracteres');
           $('#modalError').modal("show");
       }
       else if($('#TutorPassword').val().trim()!= $('#TutorPasswordRep').val().trim()){
           $('#textoErrorModal').html('Los password no coinciden, por favor verifique e intente nuevamente');
           $('#modalError').modal("show");
       }
       else if($('#pregunta').val()==""){
           $('#textoErrorModal').html('Para registrarse seleccione una pregunta de seguridad');
           $('#modalError').modal("show");
       }
       else if($('#respuesta').val().trim()==""){
            $('#textoErrorModal').html('Para registrarse escriba la respuesta a la pregunta de seguridad');
            $('#modalError').modal("show");
          }
       else{
          $.ajax({
                  async: true,
                  type: "POST",
                  url: url+"/agregarTutor",
                  dataType: 'json',
                  data: {   rut: $('#rut').val()+'-'+$('#validador').val(),
                            codColegio: $('#codColegio').val(),
                            codUsuario: $('#codUsuario').val(),
                            email: $('#email').val(),
                            nombres: $('#TutorNombres').val(),
                            apellidos: $('#TutorApellidos').val(),
                            telefono: $('#telefono').val(),
                            password: $('#TutorPassword').val(),
                            pregunta: $('#pregunta').val(),
                            respuesta: $('#respuesta').val()
                          },
                  success: function(respuesta){
                        if(respuesta.rut=='existe'){
                            if (pais=='cl'){
                                $('#textoErrorModal').html('El rut ingresado ya se encuentra inscrito en EMAT');
                            }
                            else{
                                $('#textoErrorModal').html('El Id usuario ingresado ya se encuentra inscrito en EMAT');
                                }
                          $('#modalError').modal("show");
                        }
                        else  if(respuesta.rbd==false){
                          $('#textoErrorModal').html('El código de colegio ingresado no es válido');
                          $('#modalError').modal("show");
                        }
                        else  if(respuesta.codUser=='existe'){
                          $('#textoErrorModal').html('El código de usuario ingresado no es válido');
                          $('#modalError').modal("show");
                        }
                        else  if(respuesta.status=='error1'){
                          $('#textoErrorModal').html('Ha ocurrido un error al ingresar el Tutor, Verifique e intente nuevamente');
                          $('#modalError').modal("show");
                        }
                        else  if(respuesta.status=='error2'){
                          $('#textoErrorModal').html('Ha ocurrido un error con el código usuario, Verifique e intente nuevamente');
                          $('#modalError').modal("show");
                        }
                        else{
                           $('#textoOkModal').html(respuesta.password);
                            $('#modalOk').modal("show");
                           regresaIndex();
                        }
                      },
                  error: function(){
                     $('#modalError').modal("show");
                     $('#textoErrorModal').html('Error al Registrar al Tutor');
                  }
                });
        }

 });
 }

 function regresaIndex(){
  $('#aceptar').on('click', function(){
    var url = getAbsolutePath();
   // console.log(url);
  $(location).attr('href',url);
  });
}

function getAbsolutePath() {
    var loc = window.location;
    var pathName = loc.pathname.substring(0, loc.pathname.lastIndexOf('/') + 1);
    return loc.href.substring(0, loc.href.length - ((loc.pathname + loc.search + loc.hash).length - pathName.length));
}
