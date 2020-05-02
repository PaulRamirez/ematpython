$( document ).ready(function() {


  $('.botonAvanzarMT').on('click', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      $(location).attr('href','visorMT');
    });

});