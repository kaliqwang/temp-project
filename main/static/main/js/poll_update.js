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

    var $existingChoices = $('#poll-choices-existing');

    $existingChoices.children('li').each(function(i){
        var cContent = $(this).data('content');
        var cPK = $(this).data('pk');
        var flavor = flavors.splice(Math.floor(Math.random() * flavors.length), 1);
        $existingChoices.append(Mustache.render(choiceInputTemplate, {
            index: i,
            pk: cPK,
            content: cContent,
            placeholder: flavor,
        }));
        count++;
    });

    var i = count;

    $('#add-choice').click(function(e){
        e.preventDefault();
        if (count < 20) {
            var flavor = flavors.splice(Math.floor(Math.random() * flavors.length), 1);
            $('#poll-choices').append(Mustache.render(choiceInputTemplate, {placeholder: flavor}));
            // $('#poll-choices > div.choice-input:last').find('button.remove-input').tooltip();
            count++;
            i++;
        } else {
            // TODO: Create red notification at top of choices indicating max 20 choices
        }
    });

    $('#poll-choices-existing').on('click','.remove-input', function(e){
        e.preventDefault();
        flavors.push($(this).data('flavor'));
        $(this).closest('.choice-input-wrapper').remove();
        count--;
    });

    $('#poll-choices').on('click','.remove-input', function(e){
        e.preventDefault();
        flavors.push($(this).data('flavor'));
        $(this).closest('.choice-input-wrapper').remove();
        count--;
    });

});
