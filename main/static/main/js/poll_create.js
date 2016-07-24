$(document).ready(function() {

    var flavors = [
        'Strawberry', 'Vanilla', 'Chocolate', 'Coffee', 'Peach', 'Mango',
        'Pistachio', 'Cinnamon', 'Butterscotch', 'Cheesecake', 'Eggnog',
        'S\'mores', 'Toffee', 'White Fudge', 'Salt Caramel', 'Black Cherry',
        'Butter Pecan', 'Green Tea', 'Cookie Dough', 'Rocky Road', 'Rum Raisin',
        'Mint Chocolate Chip', 'Peppermint Bark', 'Cookies and Cream'
    ];

    var count = 0;

    var choiceInputTemplate = $('#choice-input-template').html();
    Mustache.parse(choiceInputTemplate);

    $addChoiceButton = $addChoiceButton;

    $addChoiceButton.click(function(e){
        e.preventDefault();
        if (count < 20) {
            var flavor = flavors.splice(Math.floor(Math.random() * flavors.length), 1);
            $('#poll-choices').append(Mustache.render(choiceInputTemplate, {placeholder: flavor}));
            // $('#poll-choices > div.choice-input:last').find('button.remove-input').tooltip();
            count++;
        } else {
            // TODO: Create red notification at top of choices indicating max 20 choices
        }
    });

    $('#poll-choices').on('click','.remove-input', function(e){
        e.preventDefault();
        flavors.push($(this).data('flavor'));
        $(this).closest('.choice-input-wrapper').remove();
        count--;
    });

    $addChoiceButton.click();
    $addChoiceButton.click();
    $addChoiceButton.click();
    $addChoiceButton.click();
});
