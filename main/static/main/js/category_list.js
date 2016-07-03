$(document).ready(function() {

  var colors=[
      '#f2f3f4', '#222222',
      '#f3c300', '#875692',
      '#f38400', '#a1caf1',
      '#be0032', '#c2b280',
      '#848482', '#008856',
      '#e68fac', '#0067a5',
      '#f99379', '#604e97',
      '#f6a600', '#b3446c',
      '#dcd300', '#882d17',
      '#8db600', '#654522',
      '#e25822', '#2b3d26'
  ];

  var count = Number($("div.categories .initial-count").text());
  var i = count;

  function removeColor(c) {
      $("#datalist-color-choices").children('option:contains("' + c + '")').remove();
      colors.splice(colors.indexOf(c), 1);
  }

  function addColor(c) {
      $("#datalist-color-choices").append('<option>' + c + '</option>');
      colors.push(c);
  }

  $("input[type='color']").each(function(){
      var color = $(this).val();
      $(this).data('old', color);
      removeColor(color);
  });

  $("#add-category").click(function(e){e.preventDefault();
      if(count < 20){
          var color = colors[Math.floor(Math.random() * colors.length)];
          var el = $(
          '<div class="input-group-wrapper"><input type="hidden" name="category-' + i + '" value="new"/>' +
          '<div class="input-group">' +
            '<span class="input-group-btn">' +
              '<button type="button" class="btn btn-default remove_field" tabindex="-1"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>' +
            '</span>' +
            '<input required type="text" class="form-control" maxlength="50" name="category-' + i + '" placeholder="Category Name"/>' +
            '<span class="input-group-btn">' +
              '<input required type="color" class="form-control" list="datalist-color-choices" maxlength="7" name="category-' + i + '" value="' + color + '" style="width: 100px; border-bottom-right-radius: 4px; border-top-right-radius: 4px;"/>' +
            '</span>' +
          '</div><br />' +
          '</div>'
          )
          $(".categories").append(el);
          $("input[value='" + color + "']").data('old', color);
          removeColor(color);
          count++;
          i++;
      }
  });

  $(".categories").on("click",".remove_field", function(e){e.preventDefault();
      var color = $(this).parent().siblings('span.input-group-btn').find("input[type='color']").val();
      addColor(color);
      $(this).closest('.input-group-wrapper').remove();
      count--;
  });

  $(".categories").on("change","input[type='color']", function(e){e.preventDefault();
      var old_color = $(this).data('old');
      var new_color = $(this).val();
      addColor(old_color);
      removeColor(new_color);
      $(this).data('old', new_color);
  });

  $("#submit-form").click(function(e){e.preventDefault();
      var success = true;

      if(!$("#category-form")[0].checkValidity()) {
          $("input[type='text']").each(function() {
              if($(this).val().trim() == ""){
                  $(this).parent().addClass('has-error');
                  success = false;
              } else {
                  $(this).parent().removeClass('has-error');
              }
          });
      } else {
          var uniqueValues = [];
          $("input[type='text']").each(function() {
              if (uniqueValues.indexOf($(this).val().trim()) != -1) {
                  $(this).parent().addClass('has-error');
                  success = false;
              } else {
                  $(this).parent().removeClass('has-error');
                  uniqueValues.push($(this).val().trim());
              }
          });
      }

      if(success){
          $("#category-form").submit();
      }
  });

});
