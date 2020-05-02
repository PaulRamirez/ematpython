$( document ).ready(function() {

    $('#botonCerrar').on('click', function(e){
        e.preventDefault();
        e.stopImmediatePropagation();

        // inhabilita el boton cerrar.
        $("#botonCerrar").addClass('disabled');

        $.ajax({
            async: true,
            type: "POST",
            url: "cerrarSesion",
            success:function(data){
                window.close();
               $("#botonCerrar").removeClass('disabled');
            }
        });
    });

});