$( document ).ready(function() {

        $('a.btn-entrar-unidades').on('click', function(e){
                e.preventDefault();
                e.stopImmediatePropagation();
                iniciarActividad();
        });

});

function iniciarActividad(){

    $.ajax({
        async: true,
        type: "POST",
        url: "iniciarActividad",
        dataType: 'json',
        success:function(data){

            if(parseInt(data.estatus)==1){

                if(parseInt(data.id_fase)==2){  // la actividad actual es un MINITEST.
                     $(location).attr('href','/visores/portadaInicialMT');
                }
                else if(data.ultimaSiglasActividad == 'A1' || data.ultimaSiglasActividad == 'A2' || data.ultimaSiglasActividad == 'B2' || data.ultimaSiglasActividad == 'D2' || data.ultimaSiglasActividad == 'E2' || data.ultimaSiglasActividad == 'D1' || data.ultimaSiglasActividad == 'P1' || data.ultimaSiglasActividad == 'R1' || data.ultimaSiglasActividad == 'P2' || data.ultimaSiglasActividad == 'R2' || data.ultimaSiglasActividad == 'Q2' || data.ultimaSiglasActividad == 'S2'){
                     $(location).attr('href','/visores/portadaInicialAprendizaje');
                }
                else if(data.ultimaSiglasActividad == 'A4' || data.ultimaSiglasActividad =='Z1'  || data.ultimaSiglasActividad =='Z2'  || data.ultimaSiglasActividad =='Z4'  || data.ultimaSiglasActividad =='Z5'  || data.ultimaSiglasActividad =='Z6' || data.ultimaSiglasActividad == 'Z7' || data.ultimaSiglasActividad == 'Z8' || data.ultimaSiglasActividad == 'Z9' || data.ultimaSiglasActividad == 'Z0'){
                     $(location).attr('href','/visores/visorIntegracion');
                }
                else if(data.ultimaSiglasActividad == 'A3' || data.ultimaSiglasActividad == 'D3' || data.ultimaSiglasActividad == 'P3' || data.ultimaSiglasActividad == 'R3'){
                     $(location).attr('href','/visores/portadaInicialEvaluacion');
                }
                else if(data.ultimaSiglasActividad == 'A5' || data.ultimaSiglasActividad == 'D5' || data.ultimaSiglasActividad == 'P5' || data.ultimaSiglasActividad == 'R5'){
                     $(location).attr('href','/visores/portadaInicialRepaso');
                }
                else{
                    $(location).attr('href','visorActividad'); // temporalmente a una pantalla en blanco.
                }

            }else if(parseInt(data.estatus)==0){
                console.log(data.mensaje);
            }
        }
    });
}