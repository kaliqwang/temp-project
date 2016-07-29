$(document).ready(function() {
    // Constants
    var months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    var daysOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

    // Templates
    $eventInfoTemplate = $('#event-info-template').html();
    $monthHeaderTemplate = $('#month-header-template').html();
    $dateHeaderTemplate = $('#date-header-template').html();
    Mustache.parse($eventInfoTemplate);
    Mustache.parse($monthHeaderTemplate);
    Mustache.parse($dateHeaderTemplate);

    // Variables
    var $toggleCollapseAll = $('#toggle-collapse-all');
    var $eventList = $('#event-list');
    var $eventInfo = $('#event-info');
    var $eventInfoBox = $('#event-info-box');
    var $monthWrapper = $();
    var $dateWrapper = $();
    var currentDate = -1;
    var currentMonth = -1;

    /****************************** On Page Load ******************************/

    // Render event calender (nested months -> dates -> events structure)
    $eventList.children('li').each(function() {
        var newDate = new Date($(this).data('date-start'));
        // If month change
        if (currentMonth != newDate.getMonth()) {
            currentMonth = newDate.getMonth();
            currentDate = newDate.getDate();
            // Create new month wrapper
            $eventList.prepend(Mustache.render($monthHeaderTemplate, {
                monthName: months[currentMonth],
                monthIndex: currentMonth,
            }));
            $monthWrapper = $('#month-' + currentMonth);
            // Create new date wrapper
            $monthWrapper.prepend(Mustache.render($dateHeaderTemplate, {
                dateName: nth(currentDate),
                dayName: daysOfWeek[newDate.getDay()],
                dateIndex: currentDate,
            }));
            $dateWrapper = $('#date-' + currentDate);
        // Else, if date change
        } else if (currentDate != newDate.getDate()) {
            currentDate = newDate.getDate();
            // Create new date wrapper
            $monthWrapper.prepend(Mustache.render($dateHeaderTemplate, {
                dateName: nth(currentDate),
                dayName: daysOfWeek[newDate.getDay()],
                dateIndex: currentDate,
            }));
            $dateWrapper = $('#date-' + currentDate);
        }
        // Add (prepend) event to list
        $dateWrapper.prepend($(this));
    });
    // Show calender after render complete
    $eventList.removeAttr('hidden');

    // Select each month
    var $monthsCollapse = $('.month-wrapper');

    /***************************** Event Handlers *****************************/

    // Toggle month section show/hide (on click)
    $('.month-header').on('click', function() {
        var month = $(this).attr('id').substring(13);
        var $month = $('#month-' + month);
        $month.slideToggle(250);
    });

    // Vertically align info box with cursor height
    var viewPortHeight = $(window).height();
    $eventList.on('mousemove', function(e){
        var height = e.clientY - 100;
        var boxHeight = $eventInfoBox.height();
        if (height < 98) {
            $eventInfoBox.css('top', 98);
        } else if (height + boxHeight + 141 > viewPortHeight) {
            $eventInfoBox.css('top', '');
            $eventInfoBox.css('bottom', 141);
        } else {
            $eventInfoBox.css('top', height);
            $eventInfoBox.css('bottom', '');
        }
    });

    // Display event info in info box (on hover)
    $eventList.on('mouseenter', 'li', function(e) {
        var name = $(this).children('a').text();
        var dateStart = $(this).data('date-start');
        var timeStart = $(this).data('time-start').replace(/\./g, '');
        var dateEnd = $(this).data('date-end');
        var timeEnd = $(this).data('time-end').replace(/\./g, '');
        var isMultiDay = $(this).data('is-multi-day');
        var location = $(this).data('location');
        var details = $(this).data('details');
        var category = $(this).find('div.hidden').html();

        var dateTime = dateTimeToString(isMultiDay, dateStart, timeStart, dateEnd, timeEnd);

        $eventInfo.html(Mustache.render($eventInfoTemplate, {
            what: name,
            when: dateTime,
            where: location,
            details: details,
            category: category,
        }));
    });

    // Toggle collapse for all months (on click)
    $toggleCollapseAll.on('click', function(){
        if ($(this).data('mode') == '0') {
            $monthsCollapse.slideDown();
            $(this).text('Collapse All');
            $(this).data('mode', 1);
        } else {
            $monthsCollapse.slideUp();
            $(this).text('Expand All');
            $(this).data('mode', 0);
        }
    });

    /**************************** Helper Functions ****************************/

    // Get suffix for date d
    function nth(d) {
        var result = d.toString();
        if (d < 10) result = "&nbsp;&nbsp;" + result;
        if (d > 3 && d < 21) {
            return result + "<sup>th</sup>";
        } else {
          switch (d % 10) {
              case 1:  return result + "<sup>st</sup>";
              case 2:  return result + "<sup>nd</sup>";
              case 3:  return result + "<sup>rd</sup>";
              default: return result + "<sup>th</sup>";
          }
        }
    }

    // Format start date/time and end date/time into single string
    function dateTimeToString(isMultiDay, dateStart, timeStart, dateEnd, timeEnd) {
        var result = dateStart;
        if (isMultiDay == 'True') {
            if (timeStart) timeStart = ', ' + timeStart;
            if (timeEnd) timeEnd = ', ' + timeEnd;
            result += timeStart + ' - ' + dateEnd + timeEnd;
        } else {
            if (timeStart) {
                timeStart = ' @ ' + timeStart;
                if (timeEnd) timeEnd = ' - ' + timeEnd;
            }
            result += timeStart + timeEnd;
        }
        return result;
    }
});
