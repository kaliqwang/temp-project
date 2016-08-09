$(document).ready(function() {

    var count = 0;
    var i = count;
    var $categoryMergeForm = $('#category-merge-form');
    var $categories = $('#categories');
    var $colors = $('#datalist-color-choices');
    var target = "?";
    // Initialize list of colors
    var colors = [];
    $colors.children('option').each(function(){
        colors.push($(this).html());
    });

    // Pre-process templates
    var $confirmMergeTemplate = $('#confirm-merge-template').html();
    var $oldCategoryTemplate = $('#old-category-template').html();
    var $newCategoryTemplate = $('#new-category-template').html();
    Mustache.parse($confirmMergeTemplate);
    Mustache.parse($oldCategoryTemplate);
    Mustache.parse($newCategoryTemplate);

    var CategoryListHTML = '';

    // On page load
    function renderExistingCategories() {
      $.ajax({
        type: 'GET',
        url: '/api/categories/?page=1',
        success: function(data) {
          jQuery.each(data.results, function(i, c) {
            CategoryListHTML += Mustache.render($oldCategoryTemplate, {
                name: c.name,
                color: c.color,
                pk: c.pk,
            });

          });
          $categories.html(CategoryListHTML);
          CategoryListHTML='';
        }
      });
    }
    renderExistingCategories();

    // Helper functions
    function addColor(c) {
        $colors.append('<option>' + c + '</option>');
        colors.push(c);
    }
    function removeColor(c) {
        $colors.children('option:contains("' + c + '")').remove();
        colors.splice(colors.indexOf(c), 1);
    }
    function renderConfirmMergeTemplate() {
      $categoryMergeForm.html(Mustache.render($confirmMergeTemplate, {
        newName: $('#category-new-name').val(),
        newColor: $('#category-new-color').val(),
      }));
    }



    $('#continue-category-merge').click(function(e){
      e.preventDefault();
      // Selects the categories the user selected
      var $selectedCategories = $categories.find('input[type="checkbox"]:checked');
      if ($selectedCategories.length > 1 && $('#category-new-name').val()) {
        $selectedCategories.each(function() {
          CategoryListHTML += Mustache.render($newCategoryTemplate, {
            name: $(this).data('name'),
            color: $(this).data('color'),
            pk: $(this).val(),
          });
        });
        // Changes template of entire page
        renderConfirmMergeTemplate();
        // Inserts the categories selected onto page
        $('#selected-categories').html(CategoryListHTML);
        // Show Merge button and hide Continue button
        $(this).next().removeClass('hide');
        $(this).hide();
      } else {
        console.log("Please fill out form completely");
      }
    });
    // Merge categories
    $('#submit-merge-category-form').click(function(e){
      e.preventDefault();
      var $newName = $('#category-new-name').html().split(' ').join('%20');
      var $newColor = $('#category-new-color').data('color');
      var $selectedCategories = $('#selected-categories').children();

      $selectedCategories.each(function() {
        target = target + "category=" + $(this).data('pk') + "&";
      });
      target = target + 'new_name=' + $newName + '&new_color=' + encodeURIComponent($newColor);
      window.location.href = 'http://127.0.0.1:8000/categories/merge/' + target;
    })


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
