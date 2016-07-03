$(document).ready(function() {
  var flavors = [
    "Strawberry",
    "Vanilla",
    "Chocolate",
    "Coffee",
    "Peach",
    "Mango",
    "Pistachio",
    "Cinnamon",
    "Butterscotch",
    "Cheesecake",
    "Eggnog",
    "S'mores",
    "Toffee",
    "White Fudge",
    "Salt Caramel",
    "Black Cherry",
    "Butter Pecan",
    "Green Tea",
    "Cookie Dough",
    "Rocky Road",
    "Rum Raisin",
    "Mint Chocolate Chip",
    "Peppermint Bark",
    "Cookies and Cream"
   ];

  var x = 0;

  $("#add-choice").click(function(e){e.preventDefault();
      if(x < 20){
          var flavor = flavors.splice(Math.floor(Math.random() * flavors.length), 1);
          $(".choices").append(

            '<div class="input-group choice-field">' +
              '<input type="text" class="form-control" name="choice[]" maxlength="200" placeholder="' + flavor + '">' +
              '<span class="input-group-btn">' +
                '<button type="button" class="btn btn-default remove_field" tabindex="-1"><span class="glyphicon glyphicon-remove" aria-hidden="true"></span></button>' +
              '</span>' +
            '</div>'

          );
          x++;
      }
  });

  $(".choices").on("click",".remove_field", function(e){e.preventDefault();
      flavors.push($(this).parent().siblings('.form-control').attr('placeholder'))
      $(this).closest('.input-group').remove();
      x--;
  });

  $("#submit-form").click(function(e){e.preventDefault();
      $("#poll-form").submit()
  });

  $("#add-choice").click()
  $("#add-choice").click()
  $("#add-choice").click()
  $("#add-choice").click()
});
