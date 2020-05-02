$( document ).ready(function() {

  $('#botonPortadaInicialRepaso').on('click', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      $(location).attr('href','visorRepaso');
    });

});