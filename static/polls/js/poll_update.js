$(document).ready(function() {
    // Constants
    var flavors = [
        'Strawberry', 'Vanilla', 'Chocolate', 'Coffee', 'Peach', 'Mango',
        'Pistachio', 'Cinnamon', 'Butterscotch', 'Cheesecake', 'Eggnog',
        'S\'mores', 'Toffee', 'White Fudge', 'Salt Caramel', 'Black Cherry',
        'Butter Pecan', 'Green Tea', 'Cookie Dough', 'Rocky Road', 'Rum Raisin',
        'Mint Chocolate Chip', 'Peppermint Bark', 'Cookies and Cream'
    ];
    // Templates
    var $choiceInputTemplate = $('#choice-input-template').html();
    Mustache.parse($choiceInputTemplate);

    // Variables
    var $existingChoices = $('#poll-choices-existing');
    var $pollChoiceAdd = $('#poll-choice-add');
    var $newChoices = $('#poll-choices-new');
    var count = 0;
    var i = count;
    var editedChoicePKs = {};
    var removedChoicePKs = [];
    /****************************** On Page Load ******************************/
    $existingChoices.children('li').each(function(i){
      var choiceContent = $(this).data('content');
      var choicePK = $(this).data('choice-pk');
      var flavor = flavors.splice(Math.floor(Math.random() * flavors.length), 1);
      $existingChoices.append(Mustache.render($choiceInputTemplate, {
          index: i,
          pk: choicePK,
          content: choiceContent,
          placeholder: flavor,
      }));
      count++;
    });


    /***************************** Event Handlers *****************************/

    $pollChoiceAdd.click(function(e){
      e.preventDefault();
      if (count < 20) {
          var flavor = flavors.splice(Math.floor(Math.random() * flavors.length), 1);
          $newChoices.append(Mustache.render($choiceInputTemplate, {placeholder: flavor}));
          // $('#poll-choices > div.choice-input:last').find('button.remove-input').tooltip();
          count++;
          i++;
          $newChoices.children().children(' input.choice-input').each(function() {
            $(this).attr('name', 'new-choice[]');
            console.log($(this).attr('name'));
          });
      } else {
          // TODO: Create red notification at top of choices indicating max 20 choices
      }
    });

    $newChoices.on('click','.remove-input', function(e){
      e.preventDefault();
      flavors.push($(this).data('flavor'));
      $(this).closest('.choice-input-wrapper').remove();
      count--;
    });

    $existingChoices.on('click','.remove-input', function(e){
      e.preventDefault();
      flavors.push($(this).data('flavor'));
      $(this).closest('.choice-input-wrapper').remove();
      count--;
      removedChoicePKs.push($(this).data('choice-pk'));
    });

    //Will not work if user removes choice which changes choice count
    $existingChoices.on('change', 'input.choice-input', function(e){
      e.preventDefault();
      editedChoicePKs[$(this).data('choice-pk')] = $(this).val();
      for (var key in editedChoicePKs) {
        var value = editedChoicePKs[key];
      }
    });

    $('#submit-poll-update-form').click(function(e){
      e.preventDefault();
      for (var PK in editedChoicePKs) {
        var choice = {
          poll: $existingChoices.data('poll-pk'),
          content: editedChoicePKs[PK],
        };
        $.ajax({
          type: 'PUT',
          url: '/api/choices/' + PK,
          data: choice,
          success: function() {
          }
        });
      }
      removedChoicePKs.forEach(function(removedChoicePK) {
        $.ajax({
          type: 'DELETE',
          url: '/api/choices/' + removedChoicePK,
          success: function() {
          }
        });
      });
      $('#poll-update-form').submit();
    });
});
