$( document ).ready(function() {

  $('#botonPortadaInicialEvaluacion').on('click', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      $(location).attr('href','visorEvaluacion');
    });

});