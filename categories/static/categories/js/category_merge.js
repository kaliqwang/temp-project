$(document).ready(function() {

    var count = 0;

    var $categories = $('#categories');
    var $colors = $('#datalist-color-choices');
    var target = "?";
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

    // Merge categories
    $('#submit-merge-category-form').click(function(e){
      e.preventDefault();
      var $newName = $('#category-new-name').val().split(' ').join('%20');
      var $newColor = $('#category-new-color').val();
      var $mergeCategories = $categories.find('input[type="checkbox"]');

      $mergeCategories.each(function() {
        if ($(this).prop('checked')){
          console.log($(this).val());
            target = target + "category=" + $(this).val() + "&";
        }

      });
      target = target + 'new_name=' + $newName + '&new_color=%23' + $newColor
      console.log(target);
      window.location.href = 'http://127.0.0.1:8000/categories/merge/' + target;
    });
    // Manage color list
    $categories.on('click', '.remove_field', function(e){
        e.preventDefault();
        addColor($(this).parent().siblings().find('div > span > input[type="color"]').val());
        $(this).closest('.input-group-wrapper').remove();
        count--;
    }).on('change', 'input[type="color"]', function(e){
        e.preventDefault();
        addColor($(this).data('old-value'));
        removeColor($(this).val());
        $(this).data('old-value', $(this).val());
    });

});
