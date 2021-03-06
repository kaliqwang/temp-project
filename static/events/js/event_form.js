$(document).ready(function() {

    /****************************** On Page Load ******************************/

    $('.time').timepicker({
        minTime: '6:00am',
        step: 15,
        timeFormat: 'g:i a',
    });

    $('.input-daterange').datepicker({
        inputs: $('.date'),
        todayBtn: "linked",
        toggleActive: true,
        maxViewMode: 2,
    });

});
