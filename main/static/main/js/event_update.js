$(document).ready(function() {

  $("#submit-form").click(function(e){e.preventDefault();
      var success = true;
      var $inputs = $("input.form-control, textarea.form-control");
      if(!$("#event-form")[0].checkValidity()) {
          $inputs.each(function() {
              if($(this).val().length == 0){
                  $(this).parent().addClass('has-error');
                  $(this).siblings().children().css('border-color', '#a94442');
                  success = false;
              } else {
                  $(this).parent().removeClass('has-error');
                  $(this).siblings().children().css('border-color', '#ccc');
              }
          });
      }
      if(success){
          $("#event-form").submit();
      }
  });

});
