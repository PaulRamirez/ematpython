$( document ).ready(function() {

      $('#botonPortadaFinalRepaso').on('click', function(e){
          e.preventDefault();
          e.stopImmediatePropagation();
          $(location).attr('href','/ggalbas/contenidosAlumno');
       });

});

