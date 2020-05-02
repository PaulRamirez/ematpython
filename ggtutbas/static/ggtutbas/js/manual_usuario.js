$(document).ready(function(){

    $('.boton_ver').on('click', function(e){
      e.preventDefault();
      e.stopImmediatePropagation();
      window.open($(this).data("url"), '_blank');
    });
});

