$(document).ready(function() {
    /******************************* Contants ********************************/

    var monthNames = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ];
    var dayNames = [
        'Sunday', 'Monday', 'Tuesday', 'Wednesday',
        'Thursday', 'Friday', 'Saturday'
    ];
    // var monthNames = [
    //     'Jan', 'Feb', 'Mar', 'April', 'May', 'June',
    //     'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec',
    // ];
    // var dayNames = [
    //     'Sun', 'Mon', 'Tues', 'Wed',
    //     'Thurs', 'Fri', 'Sat',
    // ];

    /******************************* Templates ********************************/

    $eventItemTemplate = $('#event-item-template').html();
    $monthItemTemplate = $('#month-item-template').html();
    $dateItemTemplate = $('#date-item-template').html();
    $eventInfoTemplate = $('#event-info-template').html();
    $infoBarTopTemplate = $('#info-bar-top-template').html();
    Mustache.parse($eventItemTemplate);
    Mustache.parse($monthItemTemplate);
    Mustache.parse($dateItemTemplate);
    Mustache.parse($eventInfoTemplate);
    Mustache.parse($infoBarTopTemplate);

    /******************************* Variables ********************************/

    // Main elements
    var $eventList = $('#event-list');
    var $monthItems = $('.month-wrapper');
    var $monthHeaders = $('.month-header');
    var $monthContents = $('.month-content');
    // Top info bar
    var $infoBarTop = $('#info-bar-top');
    var $infoBarTopContent = $('#info-bar-top-content');
    var $infoBarTopDismiss = $('#info-bar-top-dismiss');
    // Event info
    var $eventInfoWrapper = $('#event-info-wrapper');
    var $eventInfo = $('#event-info');
    var $eventInfoDismiss = $('#event-info-dismiss');
    var viewPortHeight = $(window).height();
    // Top margin
    var mastHeadHeight = 90;
    var containerMargin = 8;
    var infoBarTopHeight = 0;
    var standardPaginatorHeight = 56;
    // Bottom margin
    var footerHeight = 100;
    var footerMargin = 40;
    var simplePaginatorHeight = 56;
    // Top margin
    var eventInfoTopBoundary = mastHeadHeight + containerMargin + infoBarTopHeight + standardPaginatorHeight;
    var eventInfoBottomBoundary = footerHeight + footerMargin + simplePaginatorHeight + 1;
    // Sidebar filter
    var $sidebarFilter = $('#sidebar-filter');
    var $sidebarFilterApply = $('#sidebar-filter-apply');
    var $sidebarFilterFeedback = $('#sidebar-filter-feedback');
    var profilePK = $('#user-profile-pk').text();
    // Page info
    var previousPage = -1;
    var currentPage = 1;
    var pageCount = 1;
    var pageSize = 100;
    var extendList;
    // Simple paginator (show more)
    var $paginatorSimple = $('#paginator-simple');
    var $paginatorShowMore = $('#paginator-show-more');
    // Standard paginator (page numbers)
    var $paginatorStandard = $('#paginator-standard');
    var $paginatorPrevious = $('#paginator-previous');
    var $paginatorNext = $('#paginator-next');
    var $paginatorFirst = $('#paginator-first');
    var $paginatorLast = $('#paginator-last');
    var $paginatorPageNumbers = $('#paginator-page-numbers');
    // Paginator links
    var $paginatorLinks = $('.paginator-link');
    // Buffers
    var eventListHTML = '';
    var monthBuffer = [];
    var dateBuffer = [];
    // Buffer state
    var currentYear = -1;
    var currentMonth = -1;
    var currentDate = -1;
    var currentDay = -1;
    // Toggle all months
    var $showMoreAll = $('#show-more-all');
    // Timers
    var ajaxStart, ajaxEnd, functionStart, renderStart, functionEnd, start, end;

    /****************************** On Page Load ******************************/

    // Render event list
    renderEventListPage();
    // Initialize top info bar
    if ($infoBarTopContent.children().length > 0) showInfoBarTop();

    /*************************** Render Event List ****************************/

    // Render event list by page
    function renderEventListPage(pageNumber) {
        // TODO: put currentPage logic in here
        extendList = false;
        var target = '/api/events/';
        if (pageNumber) target = target + '?page=' + pageNumber;
        renderEventListURL(target);
    }
    // Render event list by URL
    function renderEventListURL(target) {
        if (target != null) {
            console.log('Loading Page ' + currentPage + '...');
            console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            console.log('Sending GET request to ' + target);
            ajaxStart = performance.now(); // Timestamp
            // Get events via AJAX
            $.ajax({
                type: 'GET',
                url: target,
                success: renderEventListData,
                error: function(xhr, status, error) {
                    console.log('(Error)');
                    console.log('');
                    console.log('Redirecting to first page...');
                    console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
                    // Render first page of event list
                    previousPage = currentPage;
                    currentPage = 1;
                    renderEventListPage();
                },
            });
            ajaxEnd = performance.now(); // Timestamp
            console.log('');
            console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
        }
    }
    // Render event list with given data
    function renderEventListData(data) {
        functionStart = performance.now(); // Timestamp
        console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
        console.log('');
        console.log('Rendering ( ' + data.results.length + ' / ' + data.count + ' ) events:');
        console.log('');
        // Update paginator
        $paginatorPrevious.data('target', data.previous);
        $paginatorNext.data('target', data.next);
        $paginatorShowMore.data('target', data.next);
        // Render paginator
        pageCount = Math.ceil(data.count / pageSize);
        var pageNumbersHTML = '';
        for (var i = 1; i <= pageCount; i++) {
            if (i == currentPage) {
                pageNumbersHTML += '<a href="#" id="page-' + i + '" class="paginator-link selected" data-target="' + i + '">' + i + '</a>';
            } else {
                pageNumbersHTML += '<a href="#" id="page-' + i + '" class="paginator-link" data-target="' + i + '">' + i + '</a>';
            }
        }
        $paginatorPageNumbers.html(pageNumbersHTML);
        // Render each event to HTML
        if (data.count > 0) {
            jQuery.each(data.results, function(i, e) {
                start = performance.now(); // Timestamp
                // Extract data
                var pk = e.pk;
                var absoluteURL = e.absolute_url
                var name = e.name;
                var dateStart = e.date_start;
                var isMultiDay = e.is_multi_day;
                var dateStartData = e.date_start_data;
                var timeStartData = e.time_start_data;
                var dateEndData = e.date_end_data;
                var timeEndData = e.time_end_data;
                var location = e.location;
                var details = e.details;
                var categoryData = e.category_data;
                if (categoryData) {
                    categoryName = categoryData.name;
                    categoryColor = categoryData.color;
                    categoryPK = categoryData.pk;
                } else {
                    categoryName = 'Everyone';
                    categoryColor = '#222';
                    categoryPK = '-1';
                }
                // Render entire event item
                var dateTime = dateTimeStringify(isMultiDay, dateStartData, timeStartData, dateEndData, timeEndData);
                var eventItemHTML = Mustache.render($eventItemTemplate, {
                    pk: pk,
                    absoluteURL: absoluteURL,
                    name: name,
                    dateTime: dateTime,
                    location: location,
                    details: details,
                    categoryName: categoryName,
                    categoryColor: categoryColor,
                    categoryPK: categoryPK,
                });
                // If month or date changes, flush buffer
                var d = new Date(dateStart);
                if (i != 0) {
                    if (d.getDate() != currentDate) flushDateBuffer();
                    if (d.getMonth() != currentMonth) flushMonthBuffer();
                }
                // Update buffer state
                currentYear = new Date(dateStart).getFullYear();
                currentMonth = d.getMonth();
                currentDate = d.getDate();
                currentDay = d.getDay();
                // Add event item to date buffer
                dateBuffer.push(eventItemHTML);
                end = performance.now(); // Timestamp
                console.log('Event ' + (i + 1) + ':\t\t\t' + (end - start) + ' milliseconds');
            });
            // Flush all remaining events to event list buffer
            flushDateBuffer();
            flushMonthBuffer();
            renderStart = performance.now(); // Timestamp
            // Flush entire event list buffer (HTML) to DOM
            if (extendList == true) {$eventList.append(eventListHTML)}
            else {$eventList.html(eventListHTML)}
            // Clear event list buffer
            eventListHTML = '';
            // Update selectors TODO: use document.getElementsByClassName() to enable auto-updating
            $monthItems = $('.month-wrapper');
            $monthHeaders = $('.month-header');
            $monthContents = $('.month-content');
            // Maintain state consistency
            var state = $showMoreAll.data('state'); // 0 = collapsed, 1 = expanded
            if (state == 0) $monthContents.hide();
        }
        functionEnd = performance.now(); // Timestamp
        console.log('');
        console.log('Writing to DOM:\t\t' + (functionEnd - renderStart) + ' milliseconds');
        console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    }
    // Flush events from date buffer
    function flushDateBuffer() {
        var bufferContents = '';
        jQuery.each(dateBuffer, function(i, e) {bufferContents += e});
        dateItemHTML = Mustache.render($dateItemTemplate, {
            date: nth(currentDate),
            day: dayNames[currentDay],
            contents: bufferContents,
        });
        // Add date to month buffer
        monthBuffer.push(dateItemHTML);
        // Clear date buffer
        dateBuffer = [];
    }
    // Flush dates from month buffer
    function flushMonthBuffer() {
        var bufferContents = '';
        jQuery.each(monthBuffer, function(i, d){bufferContents += d});
        monthItemHTML = Mustache.render($monthItemTemplate, {
            month: currentMonth,
            monthName: monthNames[currentMonth] + ' - ' + currentYear,
            contents: bufferContents,
        });
        // Add month to event list buffer
        eventListHTML += monthItemHTML;
        // Clear month buffer
        monthBuffer = [];
    }
    // Format date / time into a single string
    function dateTimeStringify(isMultiDay, dateStart, timeStart, dateEnd, timeEnd) {
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
    // Format date d with suffix
    function nth(d) {
        var result = d.toString();
        if (d < 10) result = "&nbsp;&nbsp;" + result;
        if (d > 3 && d < 21) return result + "<sup>th</sup>";
        switch (d % 10) {
            case 1:  return result + "<sup>st</sup>";
            case 2:  return result + "<sup>nd</sup>";
            case 3:  return result + "<sup>rd</sup>";
            default: return result + "<sup>th</sup>";
        }
    }

    /****************************** Top Info Bar ******************************/

    // Dismiss top info bar
    $infoBarTopDismiss.on('click', function() {hideInfoBarTop()});
    // Show top info bar
    function showInfoBarTop() {
        $infoBarTop.show();
        infoBarTopHeight = 48;
        updateEventInfoBoundaries();
    }
    // Hide top info bar
    function hideInfoBarTop() {
        $infoBarTop.hide();
        infoBarTopHeight = 0;
        updateEventInfoBoundaries();
    }

    /******************************* Event Info *******************************/

    // Update top / bottom boundaries
    function updateEventInfoBoundaries() {
        eventInfoTopBoundary = mastHeadHeight + containerMargin + infoBarTopHeight + standardPaginatorHeight;
        eventInfoBottomBoundary = footerHeight + footerMargin + simplePaginatorHeight + 1;
        var topPos = parseInt($eventInfoWrapper.css('top').replace('px', ''));
        var bottomPos = parseInt($eventInfoWrapper.css('bottom').replace('px', ''));
        if (topPos < eventInfoTopBoundary) {
            $eventInfoWrapper.css('top', eventInfoTopBoundary);
        } else if (bottomPos < eventInfoBottomBoundary) {
            $eventInfoWrapper.css('bottom', eventInfoBottomBoundary);
        }
    }
    // Align $eventInfoWrapper with vertical position of cursor
    $eventList.on('mousemove', function(e) {
        if (true) {
            var cursorPos = e.clientY - 100;
            var eventInfoHeight = $eventInfoWrapper.height();
            if (cursorPos < eventInfoTopBoundary) {
                $eventInfoWrapper.css('bottom', '');
                $eventInfoWrapper.css('top', eventInfoTopBoundary);
            } else if (cursorPos + eventInfoHeight + eventInfoBottomBoundary > viewPortHeight) {
                $eventInfoWrapper.css('top', '');
                $eventInfoWrapper.css('bottom', eventInfoBottomBoundary);
            } else {
                $eventInfoWrapper.css('top', cursorPos);
                $eventInfoWrapper.css('bottom', '');
            }
        }
    });
    // Display event info (on hover)
    $eventList.on('mouseenter', '.event-wrapper', function(e) {e.preventDefault();
        var name = $(this).children('a').text();
        var dateTime = $(this).data('datetime');
        var location = $(this).data('location');
        var details = $(this).data('details');
        var categoryName = $(this).data('category-name');
        var categoryColor = $(this).data('category-color');
        $eventInfo.html(Mustache.render($eventInfoTemplate, {
            name: name,
            dateTime: dateTime,
            location: location,
            details: details,
            categoryName: categoryName,
            categoryColor: categoryColor,
        }));
        $eventInfo.show();
    });
    $eventInfo.on('click', '#event-info-dismiss', function() {
        console.log('click registered');
        $eventInfo.hide();
    });

    /***************************** Sidebar Filter *****************************/

    // Add / remove filters
    $sidebarFilter.on('click', '.sidebar-filter-option', function(e) {e.preventDefault();
        if ($(this).hasClass('filter-applied')) {$(this).removeClass('filter-applied')}
        else {$(this).addClass('filter-applied')}
        $sidebarFilterApply.show();
    });
    // Update filters
    $sidebarFilterApply.on('click', function(e) {e.preventDefault();
        updateFilters();
    });
    // TODO: Could this be optimized to only add/remove the most recently clicked category rather than check the whole list every time? Would that be secure / sync-safe?
    function updateFilters() {
        var $categoriesHiddenAnnouncements = $sidebarFilter.find('a.filter-applied');
        var categoriesHidden = [];
        $categoriesHiddenAnnouncements.each(function() {
            categoriesHidden.push($(this).data('pk'));
        });
        var target = '/api/user_profiles/' + profilePK
        console.log('Updating filters...')
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        console.log('Sending PUT request to ' + target);
        ajaxStart = performance.now(); // Timestamp
        $.ajax({
            type: 'PUT',
            url: target,
            data: JSON.stringify({categories_hidden_announcements: categoriesHidden}),
            contentType: 'application/json',
            success: function(data){
                functionStart = performance.now(); // Timestamp
                console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
                console.log('');
                var infoBarTopContentHTML = '';
                jQuery.each(data.categories_hidden_announcements_data, function(i, c) {
                    infoBarTopContentHTML += Mustache.render($infoBarTopTemplate, {
                        pk: c.pk,
                        categoryName: c.name,
                        categoryColor: c.color,
                    });
                    if (i == 0) {console.log('Hidden:\t\t\t\t' + c.name)}
                    else {console.log('\t\t\t\t\t' + c.name)}
                });
                if (infoBarTopContentHTML != '') {
                    $infoBarTopContent.html(infoBarTopContentHTML);
                    $infoBarTopContent.find('a').tooltip();
                    showInfoBarTop();
                    $infoBarTop.css('background-color', '#dff0d8');
                    $infoBarTop.delay(200).animate({'background-color': '#fff'}, 800);
                } else {
                    hideInfoBarTop();
                    console.log('None hidden');
                }
                $sidebarFilterApply.hide();
                $sidebarFilterFeedback.show().delay(200).fadeOut(800);
                functionEnd = performance.now(); // Timestamp
                console.log('');
                console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
                renderEventListPage();
            },
            error: function() {
                console.log('Error');
                console.log('No changes were made');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            },
        });
        ajaxEnd = performance.now(); // Timestamp
        console.log('');
        console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
    }

    /******************************* Paginator ********************************/

    // Simple paginator (show more)
    $paginatorShowMore.on('click', function(e) {e.preventDefault();
        if (currentPage < pageCount) {
            previousPage = currentPage;
            currentPage++;
            extendList = true;
            renderEventListURL($(this).data('target'));
        }
    });
    // Standard paginator (page numbers)
    $paginatorFirst.on('click', function(e) {e.preventDefault();
        previousPage = currentPage;
        currentPage = 1;
        renderEventListPage();
    });
    $paginatorLast.on('click', function(e) {e.preventDefault();
        previousPage = currentPage;
        currentPage = pageCount;
        renderEventListPage('last');
    });
    $paginatorPrevious.on('click', function(e) {e.preventDefault();
        if (currentPage > 1) {
            previousPage = currentPage;
            currentPage--;
            renderEventListURL($(this).data('target'));
        }
    });
    $paginatorNext.on('click', function(e) {e.preventDefault();
        if (currentPage < pageCount) {
            previousPage = currentPage;
            currentPage++;
            renderEventListURL($(this).data('target'), true);
        }
    });
    $paginatorPageNumbers.on('click', '.paginator-link', function(e) {e.preventDefault();
        previousPage = currentPage;
        currentPage = $(this).data('target');
        renderEventListPage(currentPage);
    });

    /*************************** Show / Hide Months ***************************/

    // Toggle single month
    $eventList.on('click', '.month-header', function(e) {e.preventDefault();
        var state = $(this).data('state'); // 0 = collapsed, 1 = expanded
        if (state == 0) {showMonth($(this))}
        else {hideMonth($(this))}
    });
    // Show month
    function showMonth($month) {
        console.log('Show month...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        start = performance.now(); // Timestamp
        $month.data('state', 1);
        $month.siblings('.month-content').show();
        end = performance.now(); // Timestamp
        console.log('Total:\t\t\t\t' + (end - start) + ' milliseconds');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    }
    // Hide month
    function hideMonth($month) {
        console.log('Hide month...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        start = performance.now(); // Timestamp
        $month.data('state', 0);
        $month.siblings('.month-content').hide();
        end = performance.now(); // Timestamp
        console.log('Total:\t\t\t\t' + (end - start) + ' milliseconds');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    }
    // Toggle all months
    $showMoreAll.on('click', function(e) {e.preventDefault();
        var state = $(this).data('state'); // 0 = collapsed, 1 = expanded
        if (state == 0) {showAllMonths()}
        else {hideAllMonths()}
    });
    // Show all months
    function showAllMonths() {
        console.log('Show all months...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        start = performance.now(); // Timestamp
        $showMoreAll.data('state', 1);
        $monthContents.each(function() {
            $(this).siblings('.month-header').data('state', 1);
            $(this).show();
        });
        $showMoreAll.children('.display-name').text('Collapse All');
        $showMoreAll.find('.glyphicon').removeClass('glyphicon-resize-full');
        $showMoreAll.find('.glyphicon').addClass('glyphicon-resize-small');
        end = performance.now(); // Timestamp
        console.log('Total:\t\t\t\t' + (end - start) + ' milliseconds');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    }
    // Hide all months
    function hideAllMonths() {
        console.log('Hide all months...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        start = performance.now(); // Timestamp
        $showMoreAll.data('state', 0);
        $monthContents.each(function() {
            $(this).siblings('.month-header').data('state', 0);
            $(this).hide();
        });
        $showMoreAll.children('.display-name').text('Expand All');
        $showMoreAll.find('.glyphicon').removeClass('glyphicon-resize-small');
        $showMoreAll.find('.glyphicon').addClass('glyphicon-resize-full');
        end = performance.now(); // Timestamp
        console.log('Total:\t\t\t\t' + (end - start) + ' milliseconds');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    }
});
