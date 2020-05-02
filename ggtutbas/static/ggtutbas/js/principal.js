$(document).ready(function(){
var url = jQuery(location).attr('href');


var path= location.pathname;
var urlActual = $('li .active').attr('href');


activarUnidad();
cambiarModoActivacion();
ordenaContenidos();

if(path == '/ggtutbas/menuPrincipal'){
    ocultarMenu();

}


    //$('#lista').val('');






    $('#lista').on('change',function(){
        var listaID = $(this).val();
        //console.log(listaID);
        if(listaID){
            mostrarMenu();
            $.ajax({
                type:'POST',
                url:'sessionCurso',
                dataType: 'json',
                data:{
                       idLista: listaID
                      },
                success:function(){
                    if (urlActual){
                        $(location).attr('href', urlActual);
                    }
                    else
                    {
                        console.log('algo paso');
                    }
                },
                error: function(){
                    console.log(url);
                }
            });
        }else{
            ocultarMenu();
        }
    });







$('#information').tooltip({
  show: { effect: "blind", duration: 800 }
});


function mostrarMenu(){
        $("li").not("#menuLogin").removeClass('menu-disabled');
    }

function ocultarMenu(){
        $("li").not("#menuLogin").addClass('menu-disabled');
    }

function ordenaContenidos(){

    var contenidos= $('#nombre_contenido, #descripcion-contenido');
    var listadeElementos= contenidos.children();


    var funcionOrdena = function(event, ui){ console.log(listadeElementos);}

    contenidos.sortable({
        connectWith: ".contenidos",
        placeholder: "placeholder",
        items: "div:not(.ui-state-disabled)",
        update: function(event, ui ){
                    $(this).children().each(function(index, unidad){
                if ($(this).attr('data-position') != (index+1)) {
                    $(this).attr('data-position', (index+1)).addClass('updated');
                    //console.log($(this).prev().attr('data-unidad'));
                }

                //console.log($(this).parents().attr('data-algo'));
                if ($(this).attr('data-unidad') != $(this).parents().attr('data-algo')) {
                    $(this).attr('data-unidad', $(this).parents().attr('data-algo')).addClass('updated');
                    //console.log($(this).prev().attr('data-unidad'));
                }
        });

        }
    });
                $('#guarda-orden').on('click', function(e){
                e.preventDefault();
                e.stopImmediatePropagation();
                var x=1;
                var y=5;

        for (var i = 0; i < contenidos.sortable().length; i++) {
            if(contenidos.sortable()[i].childElementCount==0){
                $('.updated').addClass('cancel');
                $('.updated').removeClass('updated');
                $('#textoErrorModal').html('No pueden quedar unidades vacías o con más de 5 contenidos. Revisa tu planificación.');
                $('#modalError').modal("show");
               x=contenidos.sortable()[i].children.length;
            }
            if (contenidos.sortable()[i].childElementCount>5){
                //$('#nombre_contenido,#descripcion-contenido').sortable("cancel");
                $('.updated').addClass('cancel');
                $('.updated').removeClass('updated');
                $('#textoErrorModal').html('No pueden quedar unidades vacías o con más de 5 contenidos. Revisa tu planificación.');
                $('#modalError').modal("show");
                y=contenidos.sortable()[i].children.length;
                }
        }
        var positions = [];
        $('.updated').each(function () {
        positions.push([$(this).attr('data-contenido'),$(this).attr('data-unidad'), $(this).attr('data-position')]);
        $(this).removeClass('updated');
        });
        saveNewPositions(positions, x, y);
        });
}
function saveNewPositions(positions, x, y){
    var url = jQuery(location).attr('href');

    if ((x==1) && (y<=5)){
                    $('.cancel').each(function () {
                    positions.push([$(this).attr('data-contenido'),$(this).attr('data-unidad'), $(this).attr('data-position')]);
                    $(this).removeClass('cancel');
                    });
}
if (positions!=''){

$.ajax({
               url: url+"/ordenPosicion",
               method: 'POST',
               dataType: 'json',
               data: {
                   update: 1,
                   'positions[]':JSON.stringify(positions)
               }, success: function (response) {
               console.log(response);
                    if (!response.plan){
                        $('#textoOkModal').html('hay alumnos que iniciaron el contenido que reordenaste. Ingresa nuevamente para organizar los contenidos disponibles');
                        $('#modalOk').modal("show");
                        regresaOrden();

                    }
                    else{
                        if (response.status=='ok'){
                        $('#textoOkModal').html('La organización de los contenidos se ha realizado correctamente');
                        $('#modalOk').modal("show");
                         regresaOrden();
                    }

                    }

               },
                error: function(XMLHttpRequest, textStatus, errorThrown) {
                    console.log("Status: " + textStatus); alert("Error: " + errorThrown);
                }
            });
}
else{
console.log('aca');
}
}

function verificaOrden(contenidos){
    contenidos.each(function(){
console.log(contenidos);
    });

}

function regresaOrden(){
  $('#aceptar').on('click', function(){
    var url = getAbsolutePath();
    //console.log(window.location);
  $(location).attr('href',url);
  });
}

function getAbsolutePath() {
    var loc = window.location;
    var pathName = loc.pathname.substring(0, loc.pathname.lastIndexOf('/'));
    return loc.href.substring(0, loc.href.length - ((loc.pathname + loc.search + loc.hash).length - pathName.length));
}

function activarUnidad(){
$("td .unidad-por-activar").first().removeClass('disable');
$('.unidad-por-activar').on('click', function(){

    $.ajax({
        url: 'activaUnidad',
        method: 'POST',
        dataType: 'json',
        data: {
               idUnidad: $(this).attr('data-item')
        },
        success: function(response){
            console.log(response);
            if (response.contenido='ok'){
            $(location).attr('href', url);
            }
            else{
            console.log('ocurrio un error');
            }

        }


    });
console.log($(this).attr('data-item'));
});
}

function cambiarModoActivacion(){
$('#cambiaActiva').on('click', function(){

    $.ajax({
        url: url+'/cambiarModoActiva',
        method: 'POST',
        dataType: 'json',
        data: {
            tipo: $(this).attr('data-activa'),
            lista: $('#lista').val()
        },
        success: function(response){

        if (response.activacion){
        $(location).attr('href','activarunidades');
        }
        else{
        console.log('error');
        }
        }

    });
    console.log($('#lista').val());
});
}


});