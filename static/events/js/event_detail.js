$(document).ready(function() {
    // Templates
    $eventInfoTemplate = $('#event-info-template').html();
    Mustache.parse($eventInfoTemplate);

    // Variables
    var $eventItem = $('#event-list > li');
    var $eventInfo = $('#event-info');

    /****************************** On Page Load ******************************/

    var name = $eventItem.data('name');
    var dateStart = $eventItem.data('date-start');
    var timeStart = $eventItem.data('time-start').replace(/\./g, '');
    var dateEnd = $eventItem.data('date-end');
    var timeEnd = $eventItem.data('time-end').replace(/\./g, '');
    var isMultiDay = $eventItem.data('is-multi-day');
    var location = $eventItem.data('location');
    var details = $eventItem.data('details');
    var category = $eventItem.find('span.label')[0].outerHTML;

    var dateTime = dateTimeToString(isMultiDay, dateStart, timeStart, dateEnd, timeEnd);

    $eventInfo.html(Mustache.render($eventInfoTemplate, {
        what: name,
        when: dateTime,
        where: location,
        details: details,
        category: category,
    }));

    /**************************** Helper Functions ****************************/

    // Format start date/time and end date/time into single string
    function dateTimeToString(isMultiDay, dateStart, timeStart, dateEnd, timeEnd) {
        var result = dateStart;
        if (isMultiDay == 'True') {
            if (timeStart) {
                timeStart = ', ' + timeStart;
            }
            if (timeEnd) {
                timeEnd = ', ' + timeEnd;
            }
            result += timeStart + ' - ' + dateEnd + timeEnd;
        } else {
            if (timeStart) {
                timeStart = ' @ ' + timeStart;
                if (timeEnd) {
                    timeEnd = ' - ' + timeEnd;
                }
            }
            result += timeStart + timeEnd;
        }
        return result;
    }
});
