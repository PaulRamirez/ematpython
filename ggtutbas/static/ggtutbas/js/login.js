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

validaIngreso();

function validaIngreso(){

$('#entrar').on('click', function(){
    var codColegio = $('#codColegio').val();
    var password = $('#password').val();
    var rutCompleto = $("#rut").val().trim()+"-"+$("#validador").val().trim();
    var validacion = Fn.validaRut(rutCompleto);
    var pais= $('#pais').val().trim();

    if (codColegio==""){
         $('#errorCodigo').html('<span>Para acceder a EMAT ingrese el código colegio (RBD)</span>').fadeIn(1000);
    }
    else{
        $('#errorCodigo').fadeOut('slow');
        if (rut=="" || validador=="" ){
            if (pais=='cl'){
                $('#errorRut').html('<span>Para acceder a EMAT ingrese su Rut</span>').fadeIn(1000);
            }
            else{
                $('#errorRut').html('<span>Para acceder a EMAT ingrese su Id usuario</span>').fadeIn(1000);
            }
        }
        else{
            $('#errorRut').html('').fadeIn(1000);
            if (validacion == false){
                if (pais=='cl'){
                    $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn(1000);
                    }
                else{
                    $('#errorRut').html('<span>Debe ingresar un Id usuario</span>').fadeIn(1000);
                    }
            }
            else{
                $('#errorRut').html('').fadeIn(1000);
                if (password==""){
                $('#errorPassword').html('<span>Para acceder a EMAT ingrese su password</span>').fadeIn(1000);
                }
                else{
                    $('#errorPassword').html('').fadeIn(1000);
                    $.ajax({
                        async: true,
                        type: 'POST',
                        url: url+"validaIngreso",
                        dataType: 'json',
                        data: {
                                rut: rutCompleto,
                                codColegio: codColegio,
                                password: password
                        },
                        success: function(respuesta){
                        if (respuesta.rbd){
                        console.log('rbd bien');
                            if (respuesta.listaTutor){
                                console.log('lista ok');
                                if (respuesta.user){
                                    console.log('login correcto');
                                    $(location).attr('href',"menuPrincipal");
                                }
                                else{
                                    if (pais=='cl'){
                                        $('#errorPassword').html('<span>El rut ingresado y/o password ingresados no son válidos. Inténtelo nuevamente</span>').fadeIn(1000);
                                    }
                                    else{
                                        $('#errorPassword').html('<span>El Id usuario ingresado y/o password ingresados no son válidos. Inténtelo nuevamente</span>').fadeIn(1000);
                                    }
                                    $('#codColegio').focus();
                                }
                            }
                            else{
                                if (pais=='cl'){
                                    $('#errorPassword').html('<span>El rut ingresado no está inscrito en EMAT. Verifiquélo e intente nuevamente</span>').fadeIn(1000);
                                }
                                else {
                                $('#errorPassword').html('<span>El Id usuario ingresado no está inscrito en EMAT. Verifiquélo e intente nuevamente</span>').fadeIn(1000);
                                }
                                $('#codColegio').focus();

                            }
                        }
                        else{
                        $('#errorCodigo').html('<span>El código de colegio ingresado no es válido. Inténtelo nuevamente</span>').fadeIn(1000);
                        $('#codColegio').focus();
                        }

                        console.log(respuesta);
                        }

                    });
                }
            }
        }
    }








});


}

