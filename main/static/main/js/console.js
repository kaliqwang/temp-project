$('#p_100').on('click', function(e) {e.preventDefault();
    console.log('Generating 100 polls...');
    console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    console.log('Sending GET request to /generator/polls/100/');
    ajaxStart = performance.now(); // Timestamp
    var $selected = $(this);
    $selected.find('.glyphicon-ok').hide();
    $selected.find('.glyphicon-refresh').show();
    $.ajax({
        type: 'GET',
        url: '/generator/polls/100/',
        success: function(data) {
            functionStart = performance.now(); // Timestamp
            console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
            $selected.find('.glyphicon-refresh').hide();
            $selected.find('.glyphicon-ok').show();
            functionEnd = performance.now(); // Timestamp
            console.log('');
            console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
            console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        },
        error: function(xhr, status, error) {
            console.log('(Error)');
            console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        }
    });
    ajaxEnd = performance.now(); // Timestamp
    console.log('');
    console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
    console.log('');
    console.log('Server working...');
    console.log('');
});

$('#p_1000').on('click', function(e) {e.preventDefault();
    console.log('Generating 1000 polls...');
    console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    console.log('Sending GET request to /generator/polls/1000/');
    ajaxStart = performance.now(); // Timestamp
    var $selected = $(this);
    $selected.find('.glyphicon-ok').hide();
    $selected.find('.glyphicon-refresh').show();
    $.ajax({
        type: 'GET',
        url: '/generator/polls/1000/',
        success: function(data) {
            functionStart = performance.now(); // Timestamp
            console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
            $selected.find('.glyphicon-refresh').hide();
            $selected.find('.glyphicon-ok').show();
            functionEnd = performance.now(); // Timestamp
            console.log('');
            console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
            console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        },
        error: function(xhr, status, error) {
            console.log('(Error)');
            console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        }
    });
    ajaxEnd = performance.now(); // Timestamp
    console.log('');
    console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
    console.log('');
    console.log('Server working...');
    console.log('');
});
