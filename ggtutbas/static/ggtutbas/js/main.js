$(document).ready(function(){
var url = window.location.origin;
//alert(url);
var select;


    $.ajax({
        type:'POST',
        url:url+"/ggtutbas/menuPrincipal/consultaListas",
        dataType: 'json',
        success:function(respuesta){
            if (respuesta.pais=='cl'){
                select='Seleccione un curso';
            }
            else if (respuesta.pais=='pe'){
                select='Seleccione secci&oacute;n';
            }
            else{
                select='Seleccione un curso';
            }
            var curso= '<option value="">'+select+'</option>';
            $.each(respuesta.codigoLista, function(clave, valor){
               curso+='<option value="'+clave+'">'+valor+'</option>';
            });

            $('#lista').html(curso);
            var cod = $('#codigo-curso').html();
            $('#lista').val(cod);

               if($('#lista').val() == ''){
                   $("li").not("#menuLogin").addClass('menu-disabled');
                }else{
                    $("li").not("#menuLogin").removeClass('menu-disabled');
                }

        }
     });

    $('a.collapse-item').on('click', function(e){
        $("a.collapse-item").removeClass("active text-black");
        $(this).addClass('active text-black');
    });

   $('#sidebarToggleTop').on('click', function(){
   if ($('#accordionSidebar').hasClass('toggled')){
        $('#page-top').addClass("sidebar-toggled");
        $("#accordionSidebar").css({"width": "0", "overflow":"hidden"});



   }
   else{
            $('#page-top').removeClass("sidebar-toggled");
            $("#accordionSidebar").removeClass("toggled");
            $("#accordionSidebar").css({"width": "6.5rem", "overflow":"visible"});


   }


   });
    /*    $(window).on('resize', function(){
      var win = $(this); //this = window
      if ($(window).width() < 768) {
            $('#page-top').addClass("sidebar-toggled");
            $("#accordionSidebar").addClass("toggled");
            alert('aqui');
      }
      else {
            $('#page-top').removeClass("sidebar-toggled");
            $("#accordionSidebar").removeClass("toggled");
      }
});
*/
});

