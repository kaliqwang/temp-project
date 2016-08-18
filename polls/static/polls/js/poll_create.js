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
    var $pollChoiceAdd = $('#poll-choice-add');
    var $choiceContainer = $('#poll-choices-new');
    var count = 0;

    /***************************** Event Handlers *****************************/

    $pollChoiceAdd.click(function(e){e.preventDefault();
        if (count < 20) {
            var flavor = flavors.splice(Math.floor(Math.random() * flavors.length), 1);
            $choiceContainer.append(Mustache.render($choiceInputTemplate, {placeholder: flavor}));
            // $('#poll-choices > div.choice-input:last').find('button.remove-input').tooltip();
            count++;
        } else {
            // TODO: Create red notification at top of choices indicating max 20 choices
        }
    });

    $choiceContainer.on('click','.remove-input', function(e){
        e.preventDefault();
        flavors.push($(this).data('flavor'));
        $(this).closest('.choice-input-wrapper').remove();
        count--;
    });

    $('#submit-poll-create-form').click(function(e){e.preventDefault();
        $('#poll-create-form').submit();
        return false;
        // var registration_id = '50c88caccb1381419d276ab7def422ee7d493bddec638e3364a4d297a5bfe0d7';
        // var device = {
        //   registration_id: registration_id,
        //   name: 'Rayner',
        // }
        // $.ajax({
        //   type: 'POST',
        //   url: 'http://127.0.0.1:8000/api/device/apns/?',
        //   data: device,
        //   success: function() {
        //     console.log(registration_id);
        //   }
        // })
    });

    $pollChoiceAdd.click();
    $pollChoiceAdd.click();
    $pollChoiceAdd.click();
    $pollChoiceAdd.click();

});
