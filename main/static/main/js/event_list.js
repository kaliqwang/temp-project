$(document).ready(function() {
    // Helper function for adding suffixes to dates
    function nth(d) {
        // TODO: short circuit this function for case >3 and < 21, suffix = th
        var suffix;
        switch (d % 10) {
            case 1:  suffix = "<sup>st</sup>";
            case 2:  suffix = "<sup>nd</sup>";
            case 3:  suffix = "<sup>rd</sup>";
            default: suffix = "<sup>th</sup>";
        }
        if (d < 10) {
            return "&nbsp;&nbsp;" + d.toString() + suffix;
        }
        return d.toString() + suffix;
    }

    // Constants
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Current "wrapper" elements
    var $listWrapper = $('#events-list');
    var $monthWrapper = $();
    var $dateWrapper = $();

    // Initialize currentDate and currentMonth to -1
    var currentDate = -1;
    var currentMonth = -1;

    // Events are first rendered by django as a flat list of <li> elements inside the listWrapper.
    // For each <li> event element
    $listWrapper.children().each(function() {
        // Get date information
        var dateStart = new Date($(this).data('event-date-start'));
        var dateEnd = new Date($(this).data('event-date-end'));
        // If new month (no month wrapper yet)
        if (currentMonth != dateStart.getMonth()) {
            // Get the current month
            currentMonth = dateStart.getMonth();
            // Create new current month wrapper and prepend it to $listWrapper
            $listWrapper.prepend('<li><div id="month-header-' + currentMonth + '" class="month-header"><h2>' + months[dateStart.getMonth()] + '</h2></div><ul id="month-' + currentMonth + '" class="month-wrapper"></ul></li>');
            // Store current month wrapper in $monthWrapper
            $monthWrapper = $('#month-' + currentMonth);
            // Get the current date
            currentDate = dateStart.getDate();
            // Create new current date wrapper and prepend it to $monthWrapper (guaranteed to be current by previous step)
            $monthWrapper.prepend('<li><div class="date-header">' + nth(dateStart.getDate()) + ' - ' + daysOfWeek[dateStart.getDay()] + '</div><ul id="date-' + currentDate + '" class="date-wrapper"></ul></li>');
            // Store current date wrapper in $dateWrapper
            $dateWrapper = $('#date-' + currentDate);
        } else if (currentDate != dateStart.getDate()) { // If new date in same month (no date wrapper yet)
            // Get the current date
            currentDate = dateStart.getDate();
            // Create new current date wrapper and prepend it to $monthWrapper (guaranteed to be current by previous step)
            $monthWrapper.prepend('<li><div class="date-header">' + nth(dateStart.getDate()) + ' - ' + daysOfWeek[dateStart.getDay()] + '</div><ul id="date-' + currentDate + '" class="date-wrapper"></ul></li>');
            // Store current date wrapper in $dateWrapper
            $dateWrapper = $('#date-' + currentDate);
        }

        // prepend the event to the $dateWrapper (guaranteed to be current by previous step)
        $dateWrapper.prepend($(this));
    });

    $listWrapper.removeClass('data-hidden');

    $('.month-header').on('click', function() {
        var month = $(this).attr('id').substring(13);
        var $month = $('#month-' + month);
        $month.slideToggle(300);
    });

    $eventDetailsTemplate = $('#event-details-template').html();
    $eventDetailsCategoryTemplate = $('#event-details-category-template').html();
    Mustache.parse($eventDetailsTemplate);
    Mustache.parse($eventDetailsCategoryTemplate);

    $listWrapper.on('mouseenter', '.event', function() {
        var name = $(this).data('event-name');
        var dateStart = $(this).data('event-date-start');
        var dateEnd = $(this).data('event-date-end');
        var timeStart = $(this).data('event-time-start').replace(/\./g, '');
        var timeEnd = $(this).data('event-time-end').replace(/\./g, '');
        var isMultiDay = $(this).data('event-is-multi-day');
        var location = $(this).data('event-location');
        var details = $(this).data('event-details');
        var category = $(this).find('.event-category-label').html();

        var $details = $('#event-details');

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

        $details.html(Mustache.render($eventDetailsTemplate, {
            what: name,
            when: dateTime,
            where: location,
            details: details,
            category: category,
        }));

    });

});
