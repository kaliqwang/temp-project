$(document).ready(function() {
    var $events = $('#eventsString');
    var $eventsArray = $events.html().split(";,");
    var $eventsList = $('#events-list');
    var $firstEvent = $eventsArray[0];
    var $lastEvent = $eventsArray[$eventsArray.length - 1];
    var $date = $firstEvent.substring($firstEvent.length - 14, $firstEvent.length - 3);
    var $month = parseInt($date.trim().substring(0, 2), 10);
    var $monthArray = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
    //Adjusts for extra chars on first and last event
    $eventsArray[0] = $firstEvent.substring(1);
    $eventsArray[$eventsArray.length - 1] = $lastEvent.substring(0, $lastEvent.length - 3);

    //Appends the first event's month and date
    $eventsList.append("<h2>" + $monthArray[$month - 1] + "</h2>");
    $eventsList.append("<h5 style = 'color: #2e78ba'>" + $date + "</h5>");
    //If month of event is different, appends the new month
    //If date of event is different, appends the new date
    //Appends the event no matter what
    $eventsArray.forEach(function(event) {
        var date = event.substring(event.length - 14, event.length - 3);
        var month = parseInt(date.trim().substring(0, 2), 10);
        if (date != $date) {
            if (month != $month) {
                $eventsList.append("<h2>" + $monthArray[month - 1] + "</h2>");
                $month = month;
            }
            $eventsList.append("<h5 style = 'color: #2e78ba'>" + date + "</h5>");
            $date = date;
        }
        $eventsList.append("<li>" + event.substring(11, event.length - 14) + "</li>");
    });
});
