$(document).ready(function() {

    // Variables
    var $buttons = $('button');
    var ajaxStart, ajaxEnd, functionStart, renderStart, functionEnd, start, end;

    // Initialize tooltips
    $buttons.each(function() {
        $(this).data('toggle', 'tooltip');
        $(this).data('placement', 'top');
        $(this).tooltip();
    });

    // Announcements
    $('#a_1').on('click', function(e) {generate('announcements', 1, $(this))});
    $('#a_10').on('click', function(e) {generate('announcements', 10, $(this))});
    $('#a_100').on('click', function(e) {generate('announcements', 100, $(this))});
    $('#a_1000').on('click', function(e) {generate('announcements', 1000, $(this))});
    // Events
    $('#e_1').on('click', function(e) {generate('events', 1, $(this))});
    $('#e_10').on('click', function(e) {generate('events', 10, $(this))});
    $('#e_100').on('click', function(e) {generate('events', 100, $(this))});
    $('#e_1000').on('click', function(e) {generate('events', 1000, $(this))});
    // Polls (no votes)
    $('#p_1').on('click', function(e) {generate('polls', 1, $(this))});
    $('#p_10').on('click', function(e) {generate('polls', 10, $(this))});
    $('#p_100').on('click', function(e) {generate('polls', 100, $(this))});
    $('#p_1000').on('click', function(e) {generate('polls', 1000, $(this))});
    // Polls (w/ votes)
    $('#p_v_1').on('click', function(e) {generate('polls', 1, $(this))});
    $('#p_v_10').on('click', function(e) {generate('polls', 10, $(this))});
    $('#p_v_100').on('click', function(e) {generate('polls', 100, $(this))});
    $('#p_v_1000').on('click', function(e) {generate('polls', 1000, $(this))});
    // Student Profiles
    $('#s_1').on('click', function(e) {generate('accounts/student_profiles', 1, $(this))});
    $('#s_10').on('click', function(e) {generate('accounts/student_profiles', 10, $(this))});
    $('#s_100').on('click', function(e) {generate('accounts/student_profiles', 100, $(this))});
    $('#s_1000').on('click', function(e) {generate('accounts/student_profiles', 1000, $(this))});

    function generate(model, count, $button) {
        target = '/' + model + '/generator/' + count + '/';
        console.log('Generating ' + count + ' ' + model + '...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        console.log('Sending POST request to ' + target);
        ajaxStart = performance.now(); // Timestamp
        $button.find('.glyphicon-ok').hide();
        $button.find('.glyphicon-refresh').show();
        $.ajax({
            type: 'POST',
            url: target,
            success: function(data) {
                functionStart = performance.now(); // Timestamp
                console.log(data);

                console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
                $button.find('.glyphicon-refresh').hide();
                $button.find('.glyphicon-ok').show();
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
    }

});
