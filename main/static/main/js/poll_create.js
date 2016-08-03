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
    });

    $pollChoiceAdd.click();
    $pollChoiceAdd.click();
    $pollChoiceAdd.click();
    $pollChoiceAdd.click();

});
