
$( document ).ready(function() {

$('#entrar').attr("disabled", true);

 $.getJSON( "https://api.ipify.org?format=json", function(data) {
            $("#ip").val(data.ip);
         })
         .fail(function() {
            $.ajax( "obtenerIp" )
                  .done(function(ip) {
                   $("#ip").val( ip);
                  });
         });

$('#validador').keyup(function(e){

    var rutCompleto = $("#rut").val().trim()+"-"+$("#validador").val().trim();
    var pais= $('#pais').val().trim();
    $('#errorRut').html('').fadeOut(1000);
    $('#errorPass').html('').fadeOut(1000);
    $('#errorCaptcha').html('').fadeOut(1000);

    if($("#rut").val().trim()=="" || $("#validador").val().trim()=="" ){
        //$('#errorRut').html('<span>rut o validador vacios</span>').fadeIn(1000);
    }else if(Fn.validaRut(rutCompleto)==false){
        if (pais=='cl'){
       $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn(1000);
       }
       else{
       $('#errorRut').html('<span>Debe ingresar un Id usuario válido</span>').fadeIn(1000);
       }
    }else{

       cargaAnimacion();

       $.ajax({
          async: true,
          type: "POST",
          url: "verificaRutIp",
          dataType: 'json',
          data: {
            'ip': $("#ip").val(),
            'rut': rutCompleto
          },
          success: function(respuesta){
            quitarAnimacion();
            $('#entrar').removeAttr("disabled");
            if(respuesta.status=='validado'){
                  $('#tipoIngreso').val("soloRut");
                  $('#input-password').addClass('oculto');
                  $('#captcha').addClass('oculto');
            }
            else{
                  $('#tipoIngreso').val("completo");
                  $('#input-password').removeClass('oculto');
                  $('#password').val('');
                  $('#captcha').removeClass('oculto');
                  $('#captcha').css('display', 'flex');
                  $('#texto-captcha').val('');
            }
          },
          error: function(){
            console.log('hay un error');
          }
    });
    }

});

  $('#entrar').on('click', function(e){
    e.preventDefault();
    e.stopImmediatePropagation();
   if($("#tipoIngreso").val()=="soloRut"){
       ingresoSoloRut();
   }else if($("#tipoIngreso").val()=="completo"){
       ingresoCompleto();
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


function cargaAnimacion(){
  $('#loader').fadeIn('fast');
 }

function quitarAnimacion(){
  $('#loader').fadeOut('fast');
 }

function  ingresoSoloRut(){
   var rutCompleto = $("#rut").val().trim()+"-"+$("#validador").val().trim();
   var pais= $('#pais').val().trim();
   $('#errorRut').html('').fadeOut(1000);

  if($('#rut').val().trim() =="" || $('#validador').val().trim() ==""){
        if (pais=='cl'){
       $('#errorRut').html('<span>rut o validador vacios</span>').fadeIn(1000);
       }
       else{
       $('#errorRut').html('<span>Id usuario vacio</span>').fadeIn(1000);
       }
    }else if(Fn.validaRut(rutCompleto)==false){
    if (pais=='cl'){
       $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn(1000);
       }
       else{
       $('#errorRut').html('<span>Debe ingresar un Id usuario válido</span>').fadeIn(1000);
       }
    } else{

    cargaAnimacion();


    $.ajax({
            async: true,
            type: 'POST',
            url: "ingresoSoloRut",
            dataType: 'json',
            data: {
                    rut: rutCompleto
            },
            success: function (respuesta){
                  quitarAnimacion();
                  if(parseInt(respuesta.estatus)==1){

                        $(location).attr('href',respuesta.url_alumno);
                  }
                  else if(parseInt(respuesta.estatus)==0){
                    console.log(respuesta.mensaje)
                  }
            }
    });


    }

}

function ingresoCompleto(){
      var rutCompleto = $("#rut").val().trim()+"-"+$("#validador").val().trim();
      $('#errorRut').html('').fadeOut(1000);
      $('#errorPass').html('').fadeOut(1000);
      $('#errorCaptcha').html('').fadeOut(1000);
      var pais= $('#pais').val().trim();


    if($('#rut').val().trim() =="" || $('#validador').val().trim() ==""){
        if (pais=='cl'){
       $('#errorRut').html('<span>rut o validador vacios</span>').fadeIn(1000);
       }
       else{
       $('#errorRut').html('<span>Id usuario o validador vacios</span>').fadeIn(1000);
       }
    }else if(Fn.validaRut(rutCompleto)==false){
        if (pais=='cl'){
       $('#errorRut').html('<span>Debe ingresar un Rut válido</span>').fadeIn(1000);
       }
       else{
        $('#errorRut').html('<span>Debe ingresar un Id usuario válido</span>').fadeIn(1000);
        }
    }else if($('#password').val().trim()==""){
         $('#errorPass').html('<span> Debe ingresar su contraseña</span>').fadeIn(1000);
    }else if($('#img-captcha').text()!=$('#texto-captcha').val() || $('#texto-captcha').val().trim()=="" ){
       $('#errorCaptcha').html('<span>Ingrese los números del recuadro naranjo</span>').fadeIn(1000);
    }else{

            cargaAnimacion();

            $.ajax({
            async: true,
            type: 'POST',
            url: "ingresoCompleto",
            dataType: 'json',
            data: {
                    rut: rutCompleto,
                    password: $('#password').val(),
                    ip: $("#ip").val(),
            },
            success: function (respuesta){
                  quitarAnimacion();

                  if(parseInt(respuesta.estatus) == 1){

                        $(location).attr('href',respuesta.url_alumno);

                  } else if(parseInt(respuesta.estatus) == 0){
                     $('#errorPass').html('<span>'+respuesta.mensaje+'</span>').fadeIn(1000);
                  }
            }
          });
    }

}