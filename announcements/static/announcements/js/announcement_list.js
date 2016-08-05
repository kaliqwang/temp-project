$(document).ready(function() {
    //Test Variables
    var $sidebarAnnouncementLinkTemplate = $('#sidebar-announcement-link-template').html().trim();
    Mustache.parse($sidebarAnnouncementLinkTemplate);
    var $announcementSidebar = $('#announcement-sidebar');
    var $announcementSidebarAll = $('#announcement-sidebar-all');
    var $announcementSidebarAllItems = $('#announcement-sidebar-all-items');
    var announcementSidebarHTML = ''

    var $announcementSidebarLinkSelected = $();
    var $announcementItemSelected = $();

    var $sidebarShowMore = $('#sidebar-show-more');
    var $sidebarBackToTop = $('#sidebar-back-to-top');

    $sidebarBackToTop.on('click', function(e) {e.preventDefault();
        $(document.body).animate({scrollTop: 0}, 300);
        $announcementSidebar.animate({scrollTop: 0}, 300);
    });

    // Scroll to announcement with id=announcement-pk
    $announcementSidebar.on('click', '.announcement-sidebar-link', function(e) {e.preventDefault();
        $announcementSidebarLinkSelected.removeClass('selected');
        $announcementSidebarLinkSelected = $(this);
        $announcementSidebarLinkSelected.addClass('selected');
        $announcementSidebarLinkSelected.addClass('read');
        var targetPK = $(this).data('announcement-pk');
        var $target = $('#announcement-' + targetPK);
        $announcementItemSelected.removeClass('selected');
        $announcementItemSelected = $target;
        $announcementItemSelected.addClass('selected');
        $(document.body).animate({scrollTop: $target.offset().top - ($(window).height() / 2) + 90}, 300);
    });

    /**************************************************************************/

    // Templates
    var $announcementItemTemplate = $('#announcement-item-template').html().trim();
    var $imageItemTemplate = $('#image-item-template').html().trim();
    var $videoItemTemplate = $('#video-item-template').html().trim();
    var $videoDataTemplate = $('#video-data-template').html().trim();
    Mustache.parse($announcementItemTemplate);
    Mustache.parse($imageItemTemplate);
    Mustache.parse($videoItemTemplate);
    Mustache.parse($videoDataTemplate);

    // Variables
    var $announcementList = $('#announcement-list');
    // var $announcementListData = $('#announcement-list-data');
    var announcementListHTML = '';
    var $announcementItems = $('.announcement-wrapper');
    var $itemsCollapse = $('.start-hidden');

    var pageSize = 40;
    var pageCount = 1;
    var $paginatorSimple = $('#paginator-simple');
    var $paginatorShowMore = $('#paginator-show-more');

    var $paginatorLinks = $('.paginator-link');
    var $paginatorStandard = $('#paginator-standard');
    var $paginatorPrevious = $('#paginator-previous');
    var $paginatorNext = $('#paginator-next');
    var $paginatorFirst = $('#paginator-first');
    var $paginatorLast = $('#paginator-last');
    var $paginatorPageNumbers = $('#paginator-page-numbers');

    var $sidebarFilter = $('#sidebar-filter');
    var $sidebarFilterApply = $('#sidebar-filter-apply');
    var $sidebarFilterFeedback = $('#sidebar-filter-feedback');

    var $InfoBarTop = $('#info-bar-top');
    var $InfoBarTopContent = $('#info-bar-top-content');
    var $InfoBarTopDismiss = $('#info-bar-top-dismiss');

    var $showMoreAll = $('#show-more-all');

    var profilePK = $('#user-profile-pk').text();

    /****************************** On Page Load ******************************/

    renderAnnouncementListPageNumber();
    if ($InfoBarTopContent.children().length > 0) {
        $InfoBarTop.show();
    }

    /***************************** Event Handlers *****************************/

    // Paginator
    $paginatorShowMore.on('click', function(e){e.preventDefault();
        var newPage = $paginatorPageNumbers.data('current-page') + 1;
        if (newPage <= pageCount) {
            $paginatorPageNumbers.data('current-page', newPage);
        }
        renderAnnouncementListTarget($(this).data('target'), false);
    });
    // NOTE: New code
    $sidebarShowMore.on('click', function(e){e.preventDefault();
        var newPage = $paginatorPageNumbers.data('current-page') + 1;
        if (newPage <= pageCount) {
            $paginatorPageNumbers.data('current-page', newPage);
        }
        renderAnnouncementListTarget($paginatorShowMore.data('target'), false);
    });
    $paginatorPrevious.on('click', function(e){e.preventDefault();
        if ($(this).data('target')) {
            var newPage = $paginatorPageNumbers.data('current-page') - 1;
            $paginatorPageNumbers.data('current-page', newPage);
        }
        renderAnnouncementListTarget($(this).data('target'), true);
    });
    $paginatorNext.on('click', function(e){e.preventDefault();
        if ($(this).data('target')) {
            var newPage = $paginatorPageNumbers.data('current-page') + 1;
            $paginatorPageNumbers.data('current-page', newPage);
        }
        renderAnnouncementListTarget($(this).data('target'), true);
    });
    $paginatorFirst.on('click', function(e){e.preventDefault();
        renderAnnouncementListPageNumber();
    });
    $paginatorLast.on('click', function(e){e.preventDefault();
        renderAnnouncementListPageNumber('last');
    });
    $paginatorPageNumbers.on('click', '.paginator-link', function(e){e.preventDefault();
        renderAnnouncementListPageNumber($(this).data('target'));
    });

    // Add/remove tags in filter
    $sidebarFilter.on('click', 'li > a', function(e){e.preventDefault();
        if ($(this).hasClass('filter-applied')) {
            $(this).removeClass('filter-applied');
        } else {
            $(this).addClass('filter-applied');
        }
        $sidebarFilterApply.show();
    });

    // Apply/save filter settings
    $sidebarFilterApply.on('click', function(e){e.preventDefault();
        applyFilters();
    });

    // Dismiss info box top
    $InfoBarTopDismiss.on('click', function(e){e.preventDefault();
        $InfoBarTop.hide();
    });

    // Show-more (single announcement)
    $announcementList.on('click', '.show-more', function(){
        console.log('Show more (announcement)...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        var functionStart = performance.now();
        var $media = $(this).siblings('.announcement-media')
        var $itemsCollapseLocal = $media.find('.start-hidden');
        var $videoList = $media.find('.video-list');
        if ($videoList.data('loaded') != 1) {
            var videoListHTML = '';
            $videoList.children('li').each(function(){
                videoListHTML += Mustache.render($videoItemTemplate, {
                    videoID: $(this).data('video-id'),
                });
            });
            $videoList.append(videoListHTML);
            $videoList.data('loaded', 1);
        }
        if ($(this).data('state') != 1) {
            $(this).data('state', 1);
            $itemsCollapseLocal.show();
            $(this).text('Show Less');
        } else {
            $(this).data('state', 0);
            $itemsCollapseLocal.hide();
            $(this).text('Show More');
        }
        var functionEnd = performance.now();
        console.log('Time: ' + (functionEnd - functionStart) + ' milliseconds');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    });

    // Show-more (all announcements)
    $showMoreAll.on('click', function(e){e.preventDefault();
        console.log('Show more (all announcements)...');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        var functionStart = performance.now();
        loadVideos();
        if ($(this).data('state') != 1) {
            $(this).data('state', 1);
            $itemsCollapse.show();
            $(this).children('.display-name').text('Collapse All');
            $(this).find('.glyphicon').removeClass('glyphicon-resize-full');
            $(this).find('.glyphicon').addClass('glyphicon-resize-small');
            $('.show-more').text('Show Less');
        } else {
            $(this).data('state', 0);
            $itemsCollapse.hide();
            $(this).children('.display-name').text('Expand All');
            $(this).find('.glyphicon').removeClass('glyphicon-resize-small');
            $(this).find('.glyphicon').addClass('glyphicon-resize-full');
            $('.show-more').text('Show More');
        }
        var functionEnd = performance.now();
        console.log('Total:\t\t\t\t' + (functionEnd - functionStart) + ' milliseconds');
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
    });


    /**************************** Helper Functions ****************************/

    // Render announcement list by page number
    function renderAnnouncementListPageNumber(pageNumber) {
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
        var target = '/api/announcements/?' + queryString;
        renderAnnouncementListTarget(target, true);
    }

    // Render announcement list by target URL
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
                        var dateCreated = a.date_created_data;
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
                        $announcementSidebarAllItems.html(announcementSidebarHTML);
                    } else {
                        $announcementList.append(announcementListHTML);
                        $announcementSidebarAllItems.append(announcementSidebarHTML);
                    }
                    // Reset announcement list HTML variable
                    announcementListHTML = '';
                    announcementSidebarHTML = '';
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

    // Render announcement HTML and add to announcementListHTML string
    function renderAnnouncement(data, index) {
        if (index % 4 == 0) {
          announcementListHTML += '<div class="clearfix visible-xxl-block"></div>';
        }
        if (index % 3 == 0) {
          announcementListHTML += '<div class="clearfix visible-xl-block"></div>';
        }
        if (index % 2 == 0) {
          announcementListHTML += '<div class="clearfix visible-lg-block"></div>';
        }
          announcementListHTML += '<div class="clearfix visible-sm-block"></div>';
        announcementListHTML += Mustache.render($announcementItemTemplate, {
            pk: data.pk,
            absoluteURL: data.absoluteURL,
            title: data.title,
            dateCreated: data.dateCreated,
            timeCreated: data.timeCreated,
            categoryName: data.categoryName,
            categoryColor: data.categoryColor,
            categoryPK: data.categoryPK,
            content: data.content,
            imageList: data.imageList,
            videoList: data.videoList,
            showMore: data.showMore,
        });
        // NOTE: New code
        announcementSidebarHTML += Mustache.render($sidebarAnnouncementLinkTemplate, {
          announcementPK: data.pk,
          title: data.title,
          categoryColor: data.categoryColor,
        });
    }

    // TODO: Could this be optimized to only add/remove the most recently clicked category rather than check the whole list every time? Would that be secure / sync-safe?
    function applyFilters() {
        var target = '/api/user_profiles/' + profilePK;
        var categoriesHiddenAnnouncements = [];
        var $categoriesHiddenAnnouncements = $sidebarFilter.find('a.filter-applied');
        var InfoBarTopContentHTML = '';
        $categoriesHiddenAnnouncements.each(function(){
            categoriesHiddenAnnouncements.push($(this).data('pk'));
            InfoBarTopContentHTML += '<li><a href="#" data-pk="' + $(this).data('pk') + '" title="' + $(this).children('.display-name').text() + '" data-toggle="tooltip" data-placement="top" data-trigger="hover">' +
            '<span class="icon-container" style="color:' + $(this).children('.icon-container').css('color') + '"><span class="glyphicon glyphicon-tag"></span></span>' +
            '<!-- <span class="display-name">{{ category.name }}</span> -->' +
            '</a></li>'
        });
        var data = JSON.stringify({categories_hidden_announcements: categoriesHiddenAnnouncements});
        console.log('Applying filters...')
        console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
        console.log('Sending PUT request to ' + target);
        var ajaxStart = performance.now();
        $.ajax({
            type: 'PUT',
            url: target,
            data: data,
            contentType: 'application/json',
            success: function(data){
                var functionStart = performance.now();
                console.log('Success Callback:\t' + (functionStart - ajaxEnd) + ' milliseconds');
                console.log('');
                $sidebarFilterApply.hide();
                $sidebarFilterFeedback.show().delay(200).fadeOut(800);
                if (InfoBarTopContentHTML != '') {
                    $InfoBarTopContent.html(InfoBarTopContentHTML);
                    $InfoBarTopContent.find('a').tooltip();
                    $InfoBarTop.show();
                    $InfoBarTop.css('background-color', '#dff0d8');
                    $InfoBarTop.delay(200).animate({'background-color': '#fff'}, 800);
                } else {
                    $InfoBarTop.hide();
                }
                var categories = data.categories_hidden_announcements_data;
                if (categories.length == 0) {
                    console.log('None hidden')
                }
                for (var i = 0, len = categories.length; i < len; i++) {
                    var c = categories[i];
                    if (i == 0) {
                        console.log('Hidden:\t\t\t\t' + c.name);
                    } else {
                        console.log('\t\t\t\t\t' + c.name);
                    }
                }
                var functionEnd = performance.now();
                console.log('');
                console.log('Total:\t\t\t\t' + (functionEnd - ajaxStart) + ' milliseconds');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
                renderAnnouncementListPageNumber();
            },
            error: function() {
                console.log('Error');
                console.log('No changes were made');
                console.log('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~');
            }
        });
        var ajaxEnd = performance.now();
        console.log('');
        console.log('Server responded:\t' + (ajaxEnd - ajaxStart) + ' milliseconds');
    }

    // Load videos when expanding for first time
    function loadVideos() {
        $itemsCollapse.each(function(){
            if ($(this).data('loaded') != 1) {
                var videoListHTML = '';
                $(this).children('li').each(function(){
                    videoListHTML += Mustache.render($videoItemTemplate, {
                        videoID: $(this).data('video-id'),
                    });
                });
                $(this).append(videoListHTML);
                $(this).data('loaded', 1);
            }
        });
    }

});

// Old method (slow; server-side templating)
//
// $announcementListData.children('.announcement-data').each(function(){
//     // Extract data
//     var pk = $(this).data('pk');
//     var absoluteURL = $(this).data('absolute-url');
//     var title = $(this).data('title');
//     var dateCreated = $(this).data('date-created');
//     var timeCreated = $(this).data('time-created').replace(/\./g, '');
//     var categoryName = $(this).data('category-name');
//     var categoryColor = $(this).data('category-color');
//     var categoryPK = $(this).data('category-pk');
//     var content = $(this).data('content');
//     // Create image list and video list HTML
//     var $imageListData = $(this).find('.announcement-data-image-list');
//     var $videoListData = $(this).find('.announcement-data-video-list');
//     var $imageListHTML = '';
//     var $videoListHTML = '';
//     var showMore = '';
//     // For each .announcement-data-image
//     $imageListData.children('.announcement-data-image').each(function(){
//         // Extract image data
//         var imageURL = $(this).data('image-url');
//         var imageThumbnailURL = $(this).data('image-thumbnail-url');
//         // Render image HTML and add to imageListHTML string
//         $imageListHTML += Mustache.render($imageItemTemplate, {
//             imageURL: imageURL,
//             imageThumbnailURL: imageThumbnailURL,
//         });
//     });
//     // For each .announcement-data-video
//     $videoListData.children('.announcement-data-video').each(function(){
//         // Extract video data
//         var videoID = $(this).data('video-id');
//         // Render video HTML and add to videoListHTML string
//         $videoListHTML += Mustache.render($videoItemTemplate, {
//             videoID: videoID,
//         });
//     });
//     // Set class for '#show-more' button
//     if ($videoListHTML == '') {
//         showMore = 'hidden';
//     }
//     // Render entire announcement-item and append to #announcement-list (container)
//     $announcementList.append(Mustache.render($announcementItemTemplate, {
//         pk: pk,
//         absoluteURL: absoluteURL,
//         title: title,
//         dateCreated: dateCreated,
//         timeCreated: timeCreated,
//         categoryName: categoryName,
//         categoryColor: categoryColor,
//         categoryPK: categoryPK,
//         content: content,
//         imageList: $imageListHTML,
//         videoList: $videoListHTML,
//         showMore: showMore,
//     }));
// });
