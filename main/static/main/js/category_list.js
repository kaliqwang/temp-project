$(document).ready(function() {

    var count = 0;

    var $categories = $('#categories');
    var $colors = $('#datalist-color-choices');

    // Initialize list of colors
    var colors = [];
    $colors.children('option').each(function(){
        colors.push($(this).html());
    });

    // Pre-process templates
    var $oldCategoryTemplate = $('#old-category-template').html();
    var $newCategoryTemplate = $('#new-category-template').html();
    Mustache.parse($oldCategoryTemplate);
    Mustache.parse($newCategoryTemplate);

    // Render all currently existing categories
    $categories.children('li').each(function(i){
        var cName = $(this).data('name');
        var cColor = $(this).data('color');
        var cPK = $(this).data('pk');
        $categories.append(Mustache.render($oldCategoryTemplate, {
            index: i,
            name: cName,
            color: cColor,
            pk: cPK,
        }));
        removeColor(cColor);
        count++;
    });

    // Helper functions
    function addColor(c) {
        $colors.append('<option>' + c + '</option>');
        colors.push(c);
    }
    function removeColor(c) {
        $colors.children('option:contains("' + c + '")').remove();
        colors.splice(colors.indexOf(c), 1);
    }

    var i = count;

    // Add categories
    $('#category-add').click(function(e){
        e.preventDefault();
        if (count < 20) {
            var randomColor = colors[Math.floor(Math.random() * colors.length)];
            $categories.append(Mustache.render($newCategoryTemplate, {
                index: i,
                color: randomColor,
                pk: 'new',
            }));
            removeColor(randomColor);
            count++;
            i++;
        }
    });

    // Manage color list
    $categories.on('click', '.remove_field', function(e){
        e.preventDefault();
        addColor($(this).parent().siblings('span').children('.color-input').val());
        $(this).closest('.input-group-wrapper').remove();
        count--;
    }).on('change', '.color-input', function(e){
        e.preventDefault();
        addColor($(this).data('old-value'));
        removeColor($(this).val());
        $(this).data('old-value', $(this).val());
    });

});
