$(document).ready(function() {
    var $eventDetailsWhen = $('#event-details-when');

    var dateStart = $eventDetailsWhen.data('event-date-start');
    var dateEnd = $eventDetailsWhen.data('event-date-end');
    var timeStart = $eventDetailsWhen.data('event-time-start').replace(/\./g, '');
    var timeEnd = $eventDetailsWhen.data('event-time-end').replace(/\./g, '');
    var isMultiDay = $eventDetailsWhen.data('event-is-multi-day');

    var dateTime;

    if (isMultiDay == 'True') {
        if (timeStart) {
            timeStart = ', ' + timeStart;
        }
        if (timeEnd) {
            timeEnd = ', ' + timeEnd;
        }
        dateTime = dateStart + timeStart + ' - ' + dateEnd + timeEnd;
    } else {
        if (timeStart) {
            timeStart = ' @ ' + timeStart;
            if (timeEnd) {
                timeEnd = ' - ' + timeEnd;
            }
        }
        dateTime = dateStart + timeStart + timeEnd;
    }

    $eventDetailsWhen.html('<b>When:</b> ' + dateTime);

});
