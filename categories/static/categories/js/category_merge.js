$(document).ready(function() {

    var count = 0;
    var i = count;
    var $categoryMergeForm = $('#category-merge-form');
    var $categoryMergeSetForm = $('#category-merge-set-form');
    var $categoryMergeConfirmForm = '';
    var $backButton = '';
    var $submitButton = '';
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

    // Event Handlers
    $categoryMergeForm.on('click', '#back-category-merge-form', function() {
      $categoryMergeConfirmForm.hide();
      $categoryMergeSetForm.show();
    })

    $('#continue-category-merge').click(function(e){
      e.preventDefault();
      // Selects the categories the user selected
      var $selectedCategories = $categories.find('input[type="checkbox"]:checked');
      if ($selectedCategories.length > 1 && $('#category-new-name-input').val()) {
        $selectedCategories.each(function() {
          CategoryListHTML += Mustache.render($newCategoryTemplate, {
            name: $(this).data('name'),
            color: $(this).data('color'),
            pk: $(this).val(),
          });
        });
        if (!$categoryMergeConfirmForm) {
          console.log("confirm form doesn't exist");
          // Inserts the confirm template onto page
          renderConfirmMergeTemplate();
        } else {
          console.log("confirm form exists!");
          $categoryMergeSetForm.hide();
          $categoryMergeConfirmForm.html(Mustache.render($confirmMergeTemplate, {
            newName: $('#category-new-name-input').val(),
            newColor: $('#category-new-color-input').val(),
          }));
        }
        // Inserts the categories selected onto page
        $('#selected-categories').html(CategoryListHTML);
        $categoryMergeConfirmForm.show();
        CategoryListHTML='';
      } else {
        console.log("Please fill out form completely");
      }
    });
    // Merge categories
    $categoryMergeForm.on('click', '#submit-category-merge-form', function(e) {
      e.preventDefault();
      var $newName = $('#category-new-name').html().split(' ').join('%20');
      var $newColor = $('#category-new-color').data('color');
      var $selectedCategories = $('#selected-categories').children();

      $selectedCategories.each(function() {
        target = target + "category=" + $(this).data('pk') + "&";
      });
      target = target + 'new_name=' + $newName + '&new_color=' + encodeURIComponent($newColor);
      console.log(target);
      window.location.href = 'http://127.0.0.1:8000/categories/merge/' + target;
    });

    // Helper functions
    function renderConfirmMergeTemplate() {
      $categoryMergeForm.append(Mustache.render($confirmMergeTemplate, {
        newName: $('#category-new-name-input').val(),
        newColor: $('#category-new-color-input').val(),
      }));
      $categoryMergeSetForm.hide();
      $categoryMergeConfirmForm = $('#category-merge-confirm-form');
    }
});
