
$(document).ready(function(){
  $('.modal').modal();
  $('.tooltipped').tooltip();
  $('select').formSelect();
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
});
