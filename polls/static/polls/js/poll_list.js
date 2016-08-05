$(document).ready(function() {
    //Templates
    $pollUnvotedItemTemplate = $('#poll-unvoted-item-template');
    Mustache.parse($pollUnvotedItemTemplate);

    //Variables
    var $paginatorSimple = $('#paginator-simple');
    var $paginatorShowMore = $('#paginator-show-more');

    var $paginatorLinks = $('.paginator-link');
    var $paginatorStandard = $('#paginator-standard');
    var $paginatorPrevious = $('#paginator-previous');
    var $paginatorNext = $('#paginator-next');
    var $paginatorFirst = $('#paginator-first');
    var $paginatorLast = $('#paginator-last');
    var $paginatorPageNumbers = $('#paginator-page-numbers');
    var $pollList = $('#poll-list');

    //Helper Functions
    function renderPollListPageNumber(pageNumber) {
        var queryString = '';
        if (pageNumber) {
            queryString = 'page=' + pageNumber;
            $paginatorPageNumbers.data('current-page', pageNumber);
            if (pageNumber == 'last') {
                $paginatorPageNumbers.data('current-page', pageCount);
            }
        } else {
            $paginatorPageNumbers.data('current-page', 1);
        }
        var target = '/api/polls/?' + queryString;
        renderPollListTarget(target, true);
    }
    function renderAnnouncementListTarget(target, replace) {
        if (target != null) {
            var currentPage = $paginatorPageNumbers.data('current-page');
            // Start Timer
            console.log('Loading Page ' + currentPage + '...');
            console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            console.log('Sending GET request to ' + target);
            var ajaxStart = performance.now();
            // Ajax call
            $.ajax({
                type: 'GET',
                url: target,
                success: function(data) {
                    var functionStart = performance.now();
                    var results = data.results;
                    var resultsCount = results.length;
                    var totalCount = data.count;
                    pageCount = Math.ceil(totalCount / pageSize);
                    console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
                    console.log('');
                    console.log('Rendering ( ' + resultsCount + ' / ' + totalCount + ' ) announcements:');
                    console.log('');
                    // Render paginator
                    var pageNumbersHTML = '';
                    $paginatorPrevious.data('target', data.previous);
                    $paginatorNext.data('target', data.next);
                    $paginatorShowMore.data('target', data.next);
                    for (i = 1; i <= pageCount; i++) {
                        pageNumbersHTML += '<a href="#" class="paginator-link" data-target="' + i + '">' + i + '</a>';
                    }
                    $paginatorPageNumbers.html(pageNumbersHTML);
                    // Render announcements to HTML
                    for (var i = 0; i < resultsCount; i++) {
                        var time0 = performance.now();
                        var a = results[i];
                        // Extract data
                        var categoryName = '';
                        var categoryColor = '';
                        var categoryPK = '';
                        var pk = a.pk;
                        var absoluteURL = a.absolute_url;
                        var title = a.title;
                        var dateOpen = a.date_open_data;
                        var timeCreated = a.time_created_data.replace(/\./g, '');
                        var category = a.category_data;
                        if (category) {
                            categoryName = a.category_data.name;
                            categoryColor = a.category_data.color;
                            categoryPK = a.category_data.pk;
                        } else {
                            categoryName = 'Everyone';
                            categoryColor = '#222';
                            categoryPK = '-1';
                        }
                        var content = a.content;
                        var imageFiles = a.image_files_data;
                        var imageLinks = a.image_links_data;
                        var youTubeVideos = a.youtube_videos_data;
                        // Create image list and video list HTML
                        var $imageListHTML = '';
                        var $videoListHTML = '';
                        var showMore = '';
                        var hasExtra = false;
                        var imageCount = 0;
                        // For each image file
                        for (x = 0, xMax = imageFiles.length; x < xMax; x++) {
                            var imageFile = imageFiles[x];
                            if (imageCount == 6) {
                                $imageListHTML += '<span class="start-hidden">';
                                hasExtra = true;
                            }
                            // Render image HTML and add to imageListHTML string
                            $imageListHTML += Mustache.render($imageItemTemplate, {
                                imageURL: imageFile.image_file_url,
                                imageThumbnailURL: imageFile.image_file_thumbnail_url,
                            });
                            imageCount++;
                        }
                        // For each image link
                        for (y = 0, yMax = imageLinks.length; y < yMax; y++) {
                            var imageLink = imageLinks[y];
                            if (imageCount == 6) {
                                $imageListHTML += '<span class="start-hidden">';
                                hasExtra = true;
                            }
                            // Render image HTML and add to imageListHTML string
                            $imageListHTML += Mustache.render($imageItemTemplate, {
                                imageURL: imageLink.image_file_url,
                                imageThumbnailURL: imageLink.image_file_thumbnail_url,
                            });
                            imageCount++;
                        }
                        if (hasExtra) {
                            $imageListHTML += '</span>'
                        }
                        // For each youtube video
                        for (var z = 0, zMax = youTubeVideos.length; z < zMax; z++) {
                            hasExtra = true;
                            var youTubeVideo = youTubeVideos[z];
                            // Render image HTML and add to imageListHTML string
                            $videoListHTML += Mustache.render($videoDataTemplate, {
                                videoID: youTubeVideo.youtube_video,
                            });
                        }
                        // Set class for '#show-more' button
                        if (!hasExtra) showMore = 'hidden';
                        var time1 = performance.now();
                        // Render entire announcement and add to announcement list HTML string
                        renderAnnouncement({
                            pk: pk,
                            absoluteURL: absoluteURL,
                            title: title,
                            dateCreated: dateCreated,
                            timeCreated: timeCreated,
                            categoryName: categoryName,
                            categoryColor: categoryColor,
                            categoryPK: categoryPK,
                            content: content,
                            imageList: $imageListHTML,
                            videoList: $videoListHTML,
                            showMore: showMore,
                        }, i);
                        var time2 = performance.now();

                        console.log('Announcement ' + (i + 1) + ': \t' + (time2 - time0) + ' milliseconds');
                        // console.log('\tProcessing:\t\t\t' + (time1 - time0) + ' milliseconds');
                        // console.log('\tRender:\t\t\t\t' + (time2 - time1) + ' milliseconds');
                    }
                    var render = performance.now();
                    // Write entire announcement list HTML to DOM
                    if (replace) {
                        $announcementList.html(announcementListHTML);
                        $announcementSidebar.html(announcementSidebarHTML);
                    } else {
                        $announcementList.append(announcementListHTML);
                        $announcementSidebar.append(announcementSidebarHTML);
                    }
                    // Reset announcement list HTML variable
                    announcementListHTML = '';
                    // Update current page number (paginator)
                    var currentPage = $paginatorPageNumbers.data('current-page');
                    $paginatorPageNumbers.children('.selected').removeClass('selected');
                    $paginatorPageNumbers.children(':nth-child(' + currentPage + ')').addClass('selected');
                    // Update variables TODO: use document.getElementsByClassName() to enable auto-updating
                    $announcementItems = $announcementList.children('.announcement-wrapper');
                    $itemsCollapse = $('.start-hidden');
                    var functionEnd = performance.now();
                    console.log('');
                    console.log('Writing to DOM:\t\t' + (functionEnd - render) + ' milliseconds');
                    console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
                    console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
                },
                error: function(xhr, status, error) {
                    console.log('(Error)');
                    console.log('');
                    console.log('Will redirect to first page...');
                    console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
                    $paginatorPageNumbers.data('current-page', 1);
                    // Render first page of list
                    renderAnnouncementListPageNumber();
                }
            });
            // End Timer
            var ajaxEnd = performance.now();
            console.log('');
            console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
        }
    }
    //checks if poll is closed
    function checkClosed($poll) {
        $.ajax({
            type: 'GET',
            url: '/api/polls/' + $poll.attr('id').substring(5),
            success: function(poll) {
                if (poll.is_open) {
                    return true;
                } else {
                    return false;
                }
            }
        });
    }
    //submits vote, adjusts progress-bars, shows correct buttons and progress bars, hides choices,
    $pollList.on('click', '.submit-poll', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        if (checkClosed($poll) == false) {
            ($poll).find('.alert-danger').removeClass('hide').delay(5000).fadeOut();
        } else {
            var $submit_button = $(this);
            var $choice = $poll.find("input[name=" + $poll.attr('id') + "]:checked");
            try {
                var vote = {
                voter: $poll.parent().parent().attr('data-user'),
                choice: $choice.attr('id').substring(7),
                poll: $poll.attr('id').substring(5),
                }
                $.ajax({
                    type: 'POST',
                    url: '/api/votes/',
                    data: vote,
                    success: function() {
                        if ($poll.hasClass('submitted')) {
                            $prev_choice = $poll.find('.picked');
                            $prev_choice.removeClass('picked');
                            subtractVote($prev_choice);
                        } else {
                            //Increase the total votes of poll by 1 and marks poll and choice
                            $total_vote_count = parseInt($poll.attr('data-votes'),10) + 1;
                            $poll.attr('data-votes', $total_vote_count);
                            $poll.addClass('submitted');

                        }
                        //Sets progress bars, shows progress bars, hides choices
                        $choice.addClass('picked');
                        $.when(addVote($choice)).then(setWidths($poll));
                        $poll.find('.progress-bars').removeClass('hidden');
                        $poll.find('.poll-choices').addClass('hidden');
                        $submit_button.addClass('hidden');
                        $submit_button.next().removeClass('hidden');
                    },
                });
            } catch(err) {
                $('#alert-danger').removeClass('hidden').delay(4000).fadeOut(function() {
                    $(this).addClass('hidden');
                    $(this).show();
                // $poll.find('.signature').append("<div class='alert alert-danger' style='margin-top:10px; margin-bottom:0px;'><b>Error:</b> Please select a choice.</div>");
                // $poll.find('.alert-danger').delay(4000).fadeOut(function() {
                //   $(this).remove();
                //});
              });
            }
        }
    });
    //Shows correct choices and buttons, hides progress bars
    $pollList.on('click', '.change-vote', function(e) {
        e.preventDefault();
        var $poll = $(this).closest('.poll-wrapper');
        var $submit_button = $(this).prev();
        if (checkClosed($poll) == false) {
            ($poll).find('.alert-danger').removeClass('hide').delay(5000).fadeOut();
        } else {
            //If there is no choice with class picked, find previous vote and add class picked
            if (!$poll.find('.picked').attr('class')) {
                prefillVote($poll);
            }
            $submit_button.removeClass('hidden');
            $submit_button.next().addClass('hidden');
            $poll.find('.progress-bars').addClass('hidden');
            $poll.find('.poll-choices').removeClass('hidden');
        }
    });
    /**************************** Helper Functions ****************************/
    //calculates and sets widths of progress bars
    function setWidths(poll) {
        totalVotes = poll.attr('data-votes');
        $bars = poll.find('.progress-bars').children('.progress-bar-wrapper').children('.bar-wrapper').children('.progress').children();

        $bars.each(function() {
            votes = $(this).attr('data-votes')
            $(this).css("width", votes/totalVotes*100 + "%");
            $(this).html(votes/totalVotes*100 + "%");
        });
    }
    //sets widths of all closed and voted progress bars
    function setProgressBars() {
        $closed_polls = $('#polls-closed').children();
        $voted_polls = $('#polls-voted').children();
        $closed_polls.each(function() {
            setWidths($(this));
        });
        $voted_polls.each(function() {
            setWidths($(this));
        });
    }
    setProgressBars();
    //Adjusts progress-bar and label of new choice
    function addVote($new_choice) {
        $progress_bar = $('#progress-' + $new_choice.attr('id').substring(7));
        $vote_count = parseInt($progress_bar.attr('data-votes'), 10) + 1;
        $progress_bar.attr('data-votes', $vote_count);
        $progress_bar.attr('data-original-title', $vote_count);
    }
    //Adjusts progress-bar and label of previous choice
    function subtractVote($prev_choice) {
        $progress_bar = $('#progress-' + $prev_choice.attr('id').substring(7));
        $vote_count = parseInt($progress_bar.attr('data-votes'), 10) - 1;
        $progress_bar.attr('data-votes', $vote_count);
        $progress_bar.attr('data-original-title', $vote_count);
    }
    //Finds choice previously chosen by user. Needed to adjust progress bars in voted poll.
    function prefillVote($poll) {
        $.ajax({
            type: 'GET',
            url: '/get_vote/' + ($poll).attr('id').substring(5),
            success: function(votepk) {
                $.ajax({
                    type: 'GET',
                    url: '/api/votes/' + votepk,
                    success: function(vote) {
                        $choice=$poll.find('input[id = choice-' + vote.choice + ']');
                        $choice.addClass('picked');
                    }
                });
            }
        });
    }
});
