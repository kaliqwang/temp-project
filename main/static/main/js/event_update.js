$(document).ready(function() {

    $('.time').timepicker({
        minTime: '6:00am',
        step: 15,
        timeFormat: 'g:i a',
    });

    $('.input-daterange').datepicker({
        inputs: $('.date'),
        format: 'yyyy-mm-dd',
        maxViewMode: 2,
        todayBtn: "linked",
        toggleActive: true
    });

});
