var data_table;

$(document).ready(function(){
  $('.collapsible').collapsible();
  $('.modal').modal();
  $('.tooltipped').tooltip();
  $('select').formSelect();
  $('.sidenav').sidenav();
  $('.datepicker').datepicker({
    format: 'yyyy-mm-dd',
  });
  $('.fixed-action-btn').floatingActionButton();
  //'Require' para select en HTML5
  $("select[required]").css({
    display: "inline",
    height: 0,
    padding: 0,
    width: 0
  });
  initDataTable();
});

function initDataTable(){
  //Init Datatable
  data_table = $('#table_id').DataTable({
    dom: 'Bfrtip',
    buttons: ['excel'],
    // language:{
    //   "search":         "Search:",
    //   url: "//cdn.datatables.net/plug-ins/1.10.13/i18n/Spanish.json" //Cambia idioma a español
    // },
    // "scrollY": (window.innerHeight - 500) + "px",
    paging: true,
      "oLanguage": {
        	"sProcessing":     "Procesando...",
        	"sLengthMenu":     "Mostrar _MENU_ registros",
        	"sZeroRecords":    "No se encontraron resultados",
        	"sEmptyTable":     "Ningún dato disponible en esta tabla",
        	"sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
        	"sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
        	"sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
        	"sInfoPostFix":    "",
        	"sSearch":         "Buscar en todos los camos presentes:",
        	"sUrl":            "",
        	"sInfoThousands":  ",",
        	"sLoadingRecords": "Cargando...",
        	"oPaginate": {
        		"sFirst":    "Primero",
        		"sLast":     "Último",
        		"sNext":     "Siguiente",
        		"sPrevious": "Anterior"
        	},
        	"oAria": {
        		"sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
        		"sSortDescending": ": Activar para ordenar la columna de manera descendente"
	         }
      },
    columnDefs: [
           {
               targets: [ 0, 1, 2 ],
               className: 'mdl-data-table__cell--non-numeric'
           }
       ],
  });
}

//validación de fechas
function validateFecha(id){
  var fecha_cad = document.getElementById(id);
  var dateReg = /^\d{4}[./-]\d{2}[./-]\d{2}$/;

  if(!fecha_cad.value.match(dateReg)) {
    fecha_cad.setCustomValidity("Fecha de caducidad");
  } else {
    fecha_cad.setCustomValidity('');
  }
}
