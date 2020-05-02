$( document ).ready(function() {

  $('#botonPortadaInicialAprendizaje').on('click', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      $(location).attr('href','visorAprendizaje');
    });

});