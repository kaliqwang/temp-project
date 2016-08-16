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
    $('#a_1').on('click', function(e) {generate_announcements(1, $(this))});
    $('#a_10').on('click', function(e) {generate_announcements(10, $(this))});
    $('#a_100').on('click', function(e) {generate_announcements(100, $(this))});
    $('#a_1000').on('click', function(e) {generate_announcements(1000, $(this))});
    // Events
    $('#e_1').on('click', function(e) {generate_events(1, $(this))});
    $('#e_10').on('click', function(e) {generate_events(10, $(this))});
    $('#e_100').on('click', function(e) {generate_events(100, $(this))});
    $('#e_1000').on('click', function(e) {generate_events(1000, $(this))});
    // Polls (no votes)
    $('#p_1').on('click', function(e) {generate_polls(1, false, $(this))});
    $('#p_10').on('click', function(e) {generate_polls(10, false, $(this))});
    $('#p_100').on('click', function(e) {generate_polls(100, false, $(this))});
    $('#p_1000').on('click', function(e) {generate_polls(1000, false, $(this))});
    // Polls (w/ votes)
    $('#p_v_1').on('click', function(e) {generate_polls(1, true, $(this))});
    $('#p_v_10').on('click', function(e) {generate_polls(10, true, $(this))});
    $('#p_v_100').on('click', function(e) {generate_polls(100, true, $(this))});
    $('#p_v_1000').on('click', function(e) {generate_polls(1000, true, $(this))});
    // Student Profiles
    $('#s_1').on('click', function(e) {generate_users(1, 'student_profiles', $(this))});
    $('#s_10').on('click', function(e) {generate_users(10, 'student_profiles', $(this))});
    $('#s_100').on('click', function(e) {generate_users(100, 'student_profiles', $(this))});
    $('#s_1000').on('click', function(e) {generate_users(1000, 'student_profiles', $(this))});

    function generate_announcements(count, $button) {
        target = '/announcements/generator/' + count + '/';
        console.log('Generating ' + count + ' announcements...');
        generate(target, $button);
    }
    function generate_events(count, $button) {
        target = '/events/generator/' + count + '/';
        console.log('Generating ' + count + ' events...');
        generate(target, $button);
    }
    function generate_polls(count, addVotes, $button) {
        target = '/polls/generator/' + count + '/?add_votes=' + addVotes;
        var withVotes = '';
        if (addVotes) withVotes = ' with votes';
        console.log('Generating ' + count + ' polls' + withVotes + '...');
        generate(target, $button);
    }
    function generate_users(count, model, $button) {
        target = '/accounts/' + model + '/generator/' + count + '/';
        console.log('Generating ' + count + ' ' + model + '...');
        generate(target, $button);
    }

    function generate(target, $button) {
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
