$( document ).ready(function() {

        $('#botonSalir').on('click', function(){
            $(location).attr('href','/ggalbas/');
        });

     $('a.avanzarLibroAlumno').on('click', function(e){
            e.preventDefault();
            e.stopImmediatePropagation();
            $(location).attr('href','unidadesAlumno');
     });

});