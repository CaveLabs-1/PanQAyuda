
$(document).ready(function(){
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

  //Init Datatable
  $('#table_id').DataTable({
    dom: 'Bfrtip',
    // buttons: ['copy', 'csv', 'excel', 'print'],
    language:{
      url: "//cdn.datatables.net/plug-ins/1.10.13/i18n/Spanish.json" //Cambia idioma a español
    },
    // "scrollY": (window.innerHeight - 500) + "px",
    paging: true,
    columnDefs: [
           {
               targets: [ 0, 1, 2 ],
               className: 'mdl-data-table__cell--non-numeric'
           }
       ],
  });

});
