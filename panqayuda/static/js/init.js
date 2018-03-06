
$(document).ready(function(){
  $('.modal').modal();
  $('.tooltipped').tooltip();
  $('select').formSelect();
  $('.datepicker').datepicker({
    format: 'mm-dd-yyyy 00:00:00'
  });
  $('.fixed-action-btn').floatingActionButton();

  //'Require' para select en HTML5
  $("select[required]").css({
    display: "inline",
    height: 0,
    padding: 0,
    width: 0
  });
});
