// JavaScript poll_list.js
$(document).ready(function() {
  	/********************************* Temp ***********************************/

  	var $sidebarPollLinkTemplate = $('#sidebar-poll-link-template').html().trim();
    Mustache.parse($sidebarPollLinkTemplate);
    var $pollSidebar = $('#poll-sidebar');
    var $pollSidebarAll = $('#poll-sidebar-all');
    var $pollSidebarAllItems = $('#poll-sidebar-all-items');
    var pollSidebarHTML = ''

    var $pollSidebarLinkSelected = $();
    var $pollItemSelected = $();

    var $sidebarShowMore = $('#sidebar-show-more');
    var $sidebarBackToTop = $('#sidebar-back-to-top');

  	var $showNewPolls = $('#show-new-polls');
  	var $showVotedPolls = $('#show-voted-polls');
  	var $showClosedPolls = $('#show-closed-polls');

    // Side show new polls
    $showNewPolls.on('click', function(e) { e.preventDefault();
        currentPage = 1;
        is_open = true;
        is_voted = false;
        renderPollListPageNumber(1, true);
    });
    // Sidebar show voted polls
    $showVotedPolls.on('click', function(e) { e.preventDefault();
        currentPage = 1;
        is_open= true;
        is_voted= true;
        renderPollListPageNumber(1, true);
    });
    // Sidebar show closed polls
    $showClosedPolls.on('click', function(e) { e.preventDefault();
        currentPage = 1;
        is_open = false;
        is_voted = null;
        renderPollListPageNumber(1, true);
    });
    // Sidebar back to top
    $sidebarBackToTop.on('click', function(e) {e.preventDefault();
        $(document.body).animate({scrollTop: 0}, 300);
        $pollSidebar.animate({scrollTop: 0}, 300);
    });

    // Scroll to announcement with id=announcement-pk
    $pollSidebar.on('click', '.poll-sidebar-link', function(e) {e.preventDefault();
        $pollSidebarLinkSelected.removeClass('selected');
        $pollSidebarLinkSelected = $(this);
        $pollSidebarLinkSelected.addClass('selected');
        $pollSidebarLinkSelected.addClass('read');
        var targetPK = $(this).data('pk');
        var $target = $('#poll-' + targetPK);
        $pollItemSelected.removeClass('selected');
        $pollItemSelected = $target;
        $pollItemSelected.addClass('selected');
        $(document.body).animate({scrollTop: $target.offset().top - ($(window).height() / 2) + 90}, 300);
    });

    /******************************* Templates ********************************/

    $pollItemTemplate = $('#poll-item-template').html();
    $choiceOptionTemplate = $('#choice-option-template').html();
    $choiceResultTemplate = $('#choice-result-template').html();
    $infoBarTopTemplate = $('#info-bar-top-template').html();
    Mustache.parse($pollItemTemplate);
    Mustache.parse($choiceOptionTemplate);
    Mustache.parse($choiceResultTemplate);
    Mustache.parse($infoBarTopTemplate);

    /******************************* Variables ********************************/

    // Main elements
    var $pollList = $('#poll-list');
  	var pollListHTML = '';
    var $pollVoteButtons;
    // Top info bar
    var $infoBarTop = $('#info-bar-top');
    var $infoBarTopContent = $('#info-bar-top-content');
    var $infoBarTopDismiss = $('#info-bar-top-dismiss');
    // Sidebar filter
    var $sidebarFilter = $('#sidebar-filter');
    var $sidebarFilterApply = $('#sidebar-filter-apply');
    var $sidebarFilterFeedback = $('#sidebar-filter-feedback');
    var profilePK = $('#user-profile-pk').text();
    // Page info
    var previousPage = -1;
    var currentPage = 1;
    var pageCount = 1;
    var pageSize = 36;
    var is_open = true;
    var is_voted = false;
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
    // Timers
    var ajaxStart, ajaxEnd, functionStart, renderStart, functionEnd, start, end;

    /****************************** On Page Load ******************************/

    // Render poll list
    renderPollListPageNumber(1, true);
    // Initialize top info bar
    if ($infoBarTopContent.children().length > 0) showInfoBarTop();

    // Sidebar show more
    $sidebarShowMore.on('click', function(e) {e.preventDefault();
        if (currentPage < pageCount) {
            previousPage = currentPage;
            currentPage++;
            renderPollListTarget($paginatorShowMore.data('target'), false);
        }
    });

    /*************************** Render Poll List ****************************/

    // Render poll list by page
    function renderPollListPageNumber(pageNumber) {
        var target = '/api/polls/';
        if (pageNumber) target = target + '?page=' + pageNumber; // here
        renderPollListTarget(target, true);
    }
    // Render poll list by target
    function renderPollListTarget(target, replace) {
        if (target != null) {
          	// Add querystring filters
          	if (is_open == true) target += '&is_open=True';
            else if (is_open == false) target += '&is_open=False';
            if (is_voted == true) target += '&is_voted=True';
            else if (is_voted == false) target += '&is_voted=False';
          	// Set initial state of poll list
          	var initial_state = 0;
          	var buttonAction = 'Vote';
          	if (is_open == false || is_voted == true) {
                initial_state = 1;
              	buttonAction = 'Change Vote';
            }
            console.log('Loading Page ' + currentPage + '...');
            console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            console.log('Sending GET request to ' + target);
            ajaxStart = performance.now(); // Timestamp
            // Get polls via AJAX
            $.ajax({
                type: 'GET',
                url: target,
                success: function(data) {
                    functionStart = performance.now(); // Timestamp
                    console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
                    console.log('');
                    console.log('Rendering ( ' + data.results.length + ' / ' + data.count + ' ) polls:');
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
                    // Render each poll to HTML
                    jQuery.each(data.results, function(i, p) {
                        start = performance.now();
                        var pk = p.pk;
                        var absoluteURL = p.absolute_url;
                        var content = p.content;
                        var dateOpen = p.date_open_data;
                        var timeOpen = p.time_open_data.replace(/\./g, '');
                        var totalVoteCount = parseInt(p.total_vote_count);
                        var categoryName = '';
                        var categoryColor = '';
                        var categoryPK = '';
                        var category = p.category_data;
                        if (category) {
                            categoryName = p.category_data.name;
                            categoryColor = p.category_data.color;
                            categoryPK = p.category_data.pk;
                        } else {
                            categoryName = 'Everyone';
                            categoryColor = '#222';
                            categoryPK = '-1';
                        }
                        var choices = p.choices_data;
                        var choicesHTML = '';
                        // For each choice
                        for (x = 0, xMax = choices.length; x < xMax; x++) {
                            var choice = choices[x];
                            // Render choice HTML and add to choicesHTML string
                            if (initial_state == 0) { // 0 = options, 1 = results
                              	choicesHTML += Mustache.render($choiceOptionTemplate, {
                                    choicePK: choice.pk,
                                    pk: choice.poll,
                                    choiceContent: choice.content,
                                });
                            } else {
                                var widthPercent = parseInt(choice.vote_count);
                                if (totalVoteCount > 0) widthPercent = (widthPercent / totalVoteCount) * 100;
                                var votePercent = Math.round(widthPercent);
                                choicesHTML += Mustache.render($choiceResultTemplate, {
                                    choicePK: choice.pk,
                                    choiceContent: choice.content,
                                    voteCount: choice.vote_count,
                                    votePercent: votePercent,
                                    widthPercent: widthPercent,
                                });
                            }
                        }
                      	var voteButtonHiddenClass = '';
                      	// Show / hide vote button
                        if (is_open == false) {
                        	voteButtonHiddenClass = 'hidden';
                        }
                        // Render entire poll item
                        pollListHTML += Mustache.render($pollItemTemplate, {
                            pk: pk,
                            absoluteURL: absoluteURL,
                            content: content,
                            dateOpen: dateOpen,
                            timeOpen: timeOpen,
                            categoryName: categoryName,
                            categoryColor: categoryColor,
                            categoryPK: categoryPK,
                            choices: choicesHTML,
                          	buttonAction: buttonAction,
                          	voteButtonHiddenClass: voteButtonHiddenClass,
                        });
                        pollSidebarHTML += Mustache.render($sidebarPollLinkTemplate, {
                            pk: pk,
                            content: content,
                            categoryColor: categoryColor,
                        });
                        end = performance.now(); // Timestamp
                        console.log('Poll ' + (i + 1) + ': \t\t\t' + (end - start) + ' milliseconds');
                    });
                    // break
                    renderStart = performance.now(); // Timestamp
                    if (replace) {
                        $pollList.html(pollListHTML);
                        $pollSidebarAllItems.html(pollSidebarHTML);
                    }
                    else {
                        $pollList.append(pollListHTML);
                        $pollSidebarAllItems.append(pollSidebarHTML);
                    }
                    // Clear poll list HTML and poll sidebar HTML
                    pollListHTML = '';
                    pollSidebarHTML = '';
                    // Activate tooltips
                    if (!is_open || is_voted) $('.my-progress-bar').tooltip({
                        animation: false,
                        placement: 'right',
                    });
                    // Update selectors TODO: use document.getElementsByClassName() to enable auto-updating
                  	$pollVoteButtons = $pollList.find('button.poll-vote');
                  	$pollVoteButtons.each(function() {
                      $(this).data('state', initial_state);
                    })
                    functionEnd = performance.now(); // Timestamp
                    console.log('');
                    console.log('Writing to DOM:\t\t' + (functionEnd - renderStart) + ' milliseconds');
                    console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
                    console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
                },
                error: function(xhr, status, error) {
                    console.log('(Error)');
                    console.log('');
                    console.log('Redirecting to first page...');
                    console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
                    // Render first page of poll list
                    previousPage = currentPage;
                    currentPage = 1;
                    renderPollListPageNumber();
                },
            });
            ajaxEnd = performance.now(); // Timestamp
            console.log('');
            console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
        }
    }

    /****************************** Top Info Bar ******************************/

    // Dismiss top info bar
    $infoBarTopDismiss.on('click', function() {hideInfoBarTop()});
    // Show top info bar
    function showInfoBarTop() {
        $infoBarTop.show();
    }
    // Hide top info bar
    function hideInfoBarTop() {
        $infoBarTop.hide();
    }

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
                    $infoBarTopContent.find('a').tooltip({
                        animation: false,
                        placement: 'top',
                    });
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
                renderPollListPageNumber(1, true);
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
            renderPollListTarget($(this).data('target'), false);
        }
    });
    // Standard paginator (page numbers)
    $paginatorFirst.on('click', function(e) {e.preventDefault();
          previousPage = currentPage;
          currentPage = 1;
          renderPollListPageNumber(1, true);
    });
    $paginatorLast.on('click', function(e) {e.preventDefault();
        if (currentPage != pageCount) {
            previousPage = currentPage;
            currentPage = pageCount;
            renderPollListPageNumber('last', true);
        }
    });
    $paginatorPrevious.on('click', function(e) {e.preventDefault();
        if (currentPage > 1) {
            previousPage = currentPage;
            currentPage--;
            renderPollListTarget($(this).data('target'), true);
        }
    });
    $paginatorNext.on('click', function(e) {e.preventDefault();
        if (currentPage < pageCount) {
            previousPage = currentPage;
            currentPage++;
            renderPollListTarget($(this).data('target'), true);
        }
    });
    $paginatorPageNumbers.on('click', '.paginator-link', function(e) {e.preventDefault();
        pageNumber = $(this).data('target');
        if (pageNumber == 1 || currentPage != pageNumber) {
            previousPage = currentPage;
            currentPage = pageNumber;
            renderPollListPageNumber(pageNumber, true);
        }
    });

  	/***************************** Submit Votes ******************************/

    $pollList.on('click', 'button.poll-vote', function(e) { e.preventDefault();

        var state = $(this).data('state');

      	var $target = $(this).parent().siblings('.choice-container');
        var $choiceSelected = $target.find('input:checked');
		    var pk = $target.parent().data('pk');

        if (state == 0) {
          	if ($choiceSelected.length > 0) {
                var choicePK = $choiceSelected.val();
                state = 1;
                // TODO: allow voter to be blank (set automatically in api to request.user.profile)
                var vote = {
                    voter: profilePK,
                    choice: choicePK,
                    poll: pk,
                 }
                 $.ajax({
                    type: 'POST',
                    url: '/api/votes/',
                    data: vote,
                    success: function() {
                        console.log('success');
                        updateChoicesView($target, state);
                    },
                    error: function() {
                        console.log('error');
                    }
                });
                $(this).html("Change Vote");
        	} else {
                // Error: no choice selected
            }
        } else {
            state = 0;
            $(this).html("Vote");
            updateChoicesView($target, state); // pass in the state to be rendered (0 = options; 1 = results)
        }
        $(this).data('state', state); // update state of button
    });

  	function updateChoicesView($choiceContainer, state) {
    	  var pk = $choiceContainer.parent().data('pk');

      	$.ajax({
        	  type: 'GET',
          	url: '/api/polls/' + pk,
          	success: function(data) {
                var choices = data.choices_data;
              	var totalVoteCount = parseInt(data.total_vote_count);
                // For each choice
                var choicesHTML = ''
                for (x = 0, xMax = choices.length; x < xMax; x++) {
                    var choice = choices[x];
                    // Render choice HTML and add to choicesHTML string
                    if (state == 0) { // 0 = options, 1 = results
                        choicesHTML += Mustache.render($choiceOptionTemplate, {
                            choicePK: choice.pk,
                            pk: choice.poll,
                            choiceContent: choice.content,
                        });
                    } else {
                        var widthPercent = parseInt(choice.vote_count);
                        if (totalVoteCount > 0) widthPercent = (widthPercent / totalVoteCount) * 100;
                        var votePercent = Math.round(widthPercent);
                        choicesHTML += Mustache.render($choiceResultTemplate, {
                            choicePK: choice.pk,
                            choiceContent: choice.content,
                            voteCount: choice.vote_count,
                            votePercent: votePercent,
                            widthPercent: widthPercent,
                        });
                    }
                }
              	$choiceContainer.html(choicesHTML);
              	$('.my-progress-bar').tooltip({
                    animation: false,
                    placement: 'right',
                });
            },
          	error: function() {
                console.log('error getting poll');
            }
        });
    }

});
