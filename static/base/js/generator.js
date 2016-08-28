$(document).ready(function() {

    // Variables
    var ajaxStart, ajaxEnd, functionStart, renderStart, functionEnd, start, end;

    // Initialize tooltips
    // $buttons.each(function() {
    //     $(this).data('toggle', 'tooltip');
    //     $(this).data('placement', 'top');
    //     $(this).tooltip();
    // });

    // Announcements
    $('#submit-generator-announcement').on('click', function(e) {
        var $formGroup = $(this).parent().siblings().children('.form-group');
        var $icon = $formGroup.children('.glyphicon');
        var count = parseInt($formGroup.children('input').val());
        $formGroup.removeClass('has-success has-warning');
        $icon.hide();
        if (count >= 1 && count <= 999) { // TODO: provide proper error feedback otherwise:
            var target = '/announcements/generator?count=' + count;
            console.log('Generating ' + count + ' announcements...');
            generate(target, $formGroup, $icon);
        }
    });
    // Events
    $('#submit-generator-event').on('click', function(e) {
        var $formGroup = $(this).parent().siblings().children('.form-group');
        var $icon = $formGroup.children('.glyphicon');
        var count = parseInt($formGroup.children('input').val());
        $formGroup.removeClass('has-success has-warning');
        $icon.hide();
        if (count >= 1 && count <= 999) { // TODO: provide proper error feedback otherwise:
            var target = '/events/generator?count=' + count;
            console.log('Generating ' + count + ' events...');
            generate(target, $formGroup, $icon);
        }
    });
    // Polls (no votes)
    $('#submit-generator-poll-without-votes').on('click', function(e) {
        var $formGroup = $(this).parent().siblings().children('.form-group');
        var $icon = $formGroup.children('.glyphicon');
        var count = parseInt($formGroup.children('input').val());
        $formGroup.removeClass('has-success has-warning');
        $icon.hide();
        if (count >= 1 && count <= 999) { // TODO: provide proper error feedback otherwise:
            var target = '/polls/generator?count=' + count + '&add_votes=false';
            console.log('Generating ' + count + ' polls without votes...');
            generate(target, $formGroup, $icon);
        }
    });
    // Polls (w/ votes)
    $('#submit-generator-poll-with-votes').on('click', function(e) {
        var $formGroup = $(this).parent().siblings().children('.form-group');
        var $icon = $formGroup.children('.glyphicon');
        var count = parseInt($formGroup.children('input').val());
        $formGroup.removeClass('has-success has-warning');
        $icon.hide();
        if (count >= 1 && count <= 999) { // TODO: provide proper error feedback otherwise:
            var target = '/polls/generator?count=' + count + '&add_votes=true';
            console.log('Generating ' + count + ' polls with votes...');
            generate(target, $formGroup, $icon);
        }
    });
    // Student Profiles
    $('#submit-generator-student-profile').on('click', function(e) {
        var $formGroup = $(this).parent().siblings().children('.form-group');
        var $icon = $formGroup.children('.glyphicon');
        var count = parseInt($formGroup.children('input').val());
        $formGroup.removeClass('has-success has-warning');
        $icon.hide();
        if (count >= 1 && count <= 999) { // TODO: provide proper error feedback otherwise:
            var target = '/accounts/student_profiles/generator?count=' + count;
            console.log('Generating ' + count + ' student_profiles...');
            generate(target, $formGroup, $icon);
        }
    });

    // Other
    $('#submit-generator-admin-profile').on('click', function(e) {
        var data = {
            user: '1',
            mobile: '6787901506'
        }
        var target = '/api/user_profiles/'
        console.log('Generating user_profile for admin...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        console.log('Sending POST request to ' + target);
        ajaxStart = performance.now(); // Timestamp
        $.ajax({
            type: 'POST',
            url: target,
            data: data,
            success: function(data) {
                functionStart = performance.now(); // Timestamp
                console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
                console.log('Admin user_profile created successfully');
                functionEnd = performance.now(); // Timestamp
                console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            },
            error: function(xhr, status, error) {
                console.log('(Error)');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            }
        });
        ajaxEnd = performance.now(); // Timestamp
        console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
        console.log('Server working...');
    });

    $('#submit-generator-category').on('click', function(e) {
        var data = [
            {
                name: 'Academic',
                color: '#e25822',
            },
            {
                name: 'Administrative',
                color: '#848482',
            },
            {
                name: 'Extracurricular',
                color: '#f6a600',
            },
            {
                name: 'Music',
                color: '#dcd300',
            },
            {
                name: 'Publications',
                color: '#8db600',
            },
            {
                name: 'Services',
                color: '#a1caf1',
            },
            {
                name: 'Sports',
                color: '#0067a5',
            },
            {
                name: 'Student Council',
                color: '#875692',
            },
        ]
        var target = '/api/categories/'
        console.log('Generating default categories...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        console.log('Sending POST request to ' + target);
        ajaxStart = performance.now(); // Timestamp
        $.ajax({
            type: 'POST',
            url: target,
            data: data,
            success: function(data) {
                functionStart = performance.now(); // Timestamp
                console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
                console.log('Successfully generated categories:');
                jQuery.each(data, function(i, c) {
                    console.log(c.name + ' - ' + c.color);
                });
                functionEnd = performance.now(); // Timestamp
                console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            },
            error: function(xhr, status, error) {
                console.log('(Error)');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            }
        });
        ajaxEnd = performance.now(); // Timestamp
        console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
        console.log('Server working...');
    });

    function generate(target, $formGroup, $icon) {
        $formGroup.removeClass('has-success has-warning');
        $icon.removeClass('glyphicon-warning-sign glyphicon-ok');
        $icon.addClass('glyphicon-refresh');
        $icon.show();
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        console.log('Sending POST request to ' + target);
        ajaxStart = performance.now(); // Timestamp
        $.ajax({
            type: 'POST',
            url: target,
            success: function(data) {
                functionStart = performance.now(); // Timestamp
                $formGroup.addClass('has-success');
                $icon.removeClass('glyphicon-refresh');
                $icon.addClass('glyphicon-ok');
                console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
                console.log(data);
                functionEnd = performance.now(); // Timestamp
                console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            },
            error: function(xhr, status, error) {
                $formGroup.addClass('has-warning');
                $icon.removeClass('glyphicon-refresh');
                $icon.addClass('glyphicon-warning-sign');
                console.log('(Error)');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            }
        });
        ajaxEnd = performance.now(); // Timestamp
        console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
        console.log('Server working...');
    }

});
