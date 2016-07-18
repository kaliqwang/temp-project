$(document).ready(function() {

  var x = 0;
  var imageFileField = $('#image-file-template').html()
  $("#add-image-file").click(function(e){
    e.preventDefault();
    if(x < 5){
      x++;
      $("#multiple-image-files").append(imageFileField);
    }
  });
  $("#multiple-image-files").on("click",".remove_field", function(e){
    e.preventDefault();
    $(this).closest('div.input-group').remove(); x--;
  });

  var y = 0;
  var imageLinkField = $('#image-link-template').html()
  $("#add-image-link").click(function(e){
    e.preventDefault();
    if(y < 5){
      y++;
      $("#multiple-image-links").append(imageLinkField);
    }
  });
  $("#multiple-image-links").on("click",".remove_field", function(e){
    e.preventDefault();
    $(this).closest('div.input-group').remove(); y--;
  });
$("#multiple-image-links").on("change", "input", function(e) {
    e.preventDefault();
    $(this).parent().prev().append("<img src='" + $(this).val() + "'>");
});
$("#multiple-image-files").on("change", "input", function(e) {
    e.preventDefault();
    readURL(this);
});
function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        console.log("this is working as well");
        reader.onload = function (e) {
            $(input).parent().prev().append("<img src='" + e.target.result + "'>");
        }

        reader.readAsDataURL(input.files[0]);
    }
}
  // var z = 0;
  // var youtubeVideoField = $('#youtube-video-template').html()
  // $("#add-youtube-video").click(function(e){
  //   e.preventDefault();
  //   if(z < 5){
  //     z++;
  //     $("#multiple-videos").append(youtubeVideoField);
  //   }
  // });
  // $("#multiple-videos").on("click",".remove_field", function(e){
  //   e.preventDefault();
  //   $(this).closest('div.input-group').remove();
  //   z--;
  // });

  $("#submit-form").click(function(e){e.preventDefault();
      var success = true;
      var $inputs = $("input.form-control, textarea.form-control");
      if(!$("#announcement-form")[0].checkValidity()) {
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
          $("#announcement-form").submit();
      }
  });

  $("#add-youtube-video").click(function(e){
    e.preventDefault();
    if(z < 5){
      z++;
      $("#multiple-videos").append(youtubeVideoField);
    }
  });
  $("#multiple-videos").on("click",".remove_field", function(e){
    e.preventDefault();
    $(this).closest('div.input-group').remove();
    z--;
  });


});
