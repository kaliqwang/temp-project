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
            // Create new current month wrapper and append it to $listWrapper
            $listWrapper.append('<li><div id="month-header-' + currentMonth + '" class="month-header"><h2>' + months[dateStart.getMonth()] + '</h2></div><ul id="month-' + currentMonth + '" class="month-wrapper"></ul></li>');
            // Store current month wrapper in $monthWrapper
            $monthWrapper = $('#month-' + currentMonth);
        }
        // If new date (no date wrapper yet)
        if (currentDate != dateStart.getDate()) {
            // Get the current date
            currentDate = dateStart.getDate();
            // Create new current date wrapper and append it to $monthWrapper (guaranteed to be current by previous step)
            $monthWrapper.append('<li><div class="date-header">' + nth(dateStart.getDate()) + ' - ' + daysOfWeek[dateStart.getDay()] + '</div><ul id="date-' + currentDate + '" class="date-wrapper"></ul></li>');
            // Store current date wrapper in $dateWrapper
            $dateWrapper = $('#date-' + currentDate);
        }

        // Append the event to the $dateWrapper (guaranteed to be current by previous step)
        $dateWrapper.append($(this));
    });

    $listWrapper.removeClass('data-hidden');

    $('.month-header').on('click', function(e) {
        e.preventDefault();
        var month = $(this).attr('id').substring(13);
        console.log(month);
        var $month = $('#month-' + month);
        $month.slideToggle(300);
    });

});
