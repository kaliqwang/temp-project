$(document).ready(function() {

    //
    // var mediaArray = [];
    //
    // //set data-status of all mmedia to 0 meaning they can be selected
    // $('#announcement-list').on('click', '.edit-announcement', function(e) {
    //     e.preventDefault();
    //     var $announcement = $(this).closest('.announcement-wrapper');
    //     var $images = $announcement.find('.images');
    //     $announcement.addClass("edit");
    //     $images.children().attr('data-status', 0);
    // });
    // //set data-status of all mmedia to 3 meaning they can no longer be selected
    // $('#announcement-list').on('click', '.cancel-announcement', function(e) {
    //     e.preventDefault();
    //     var $announcement = $(this).closest('.announcement-wrapper');
    //     var $images = $announcement.find('.images');
    //     $announcement.removeClass("edit");
    //     $images.children().removeClass('selected');
    //     $images.children().attr('data-status', 3);
    //     $images.children().each(function() {
    //         $(this).find('span.remove').html('Remove');
    //     })
    //     mediaArray = [];
    // });
    //
    // $('#announcement-list').on('click', '.save-announcement', function(e) {
    //     e.preventDefault();
    //     var $announcement = $(this).closest('.announcement-wrapper');
    //
    //     var announcement = {
    //         author: $announcement.find('.author').text(),
    //         title: $announcement.find('.title > input').val(),
    //         category: $announcement.find('.category').text(),
    //         date_created: $announcement.find('.date_created').text(),
    //         content: $announcement.find('.content > textarea').val(),
    //         rank: $announcement.find('.rank').text(),
    //         image_files: [],
    //         image_links: [],
    //         youtube_videos: [],
    //     };
    //
    //     $.ajax({
    //         type: 'PUT',
    //         url: '/api/announcements/' + $announcement.attr('id'),
    //         data: announcement,
    //         success: function(newAnnouncement) {
    //             $announcement.find('.title > a > h2').text(newAnnouncement.title);
    //             $announcement.find('.content.noedit').text(newAnnouncement.content);
    //             $announcement.removeClass('edit');
    //         },
    //         error: function() {
    //             alert('Error updating announcement.');
    //         }
    //     });
    //
    //     mediaArray.forEach(function(media) {
    //         $.ajax({
    //             type: 'DELETE',
    //             url: '/api/' + media.attr('data-id') + '/' + media.attr('id'),
    //             success: function() {
    //                 media.fadeOut();
    //             },
    //             error: function() {
    //                 alert('Error deleting media.');
    //             }
    //         });
    //     });
    // });
    // $('#announcement-list').on('click', '.mmedia', function(e) {
    //     e.preventDefault();
    //     var $message = $(this).find('span.remove');
    //
    //     if ($(this).attr('data-status') == 0) {
    //         $(this).attr('data-status', 1);
    //         $(this).addClass('selected');
    //         mediaArray.push($(this));
    //         $message.html('Restore');
    //
    //     } else if ($(this).attr('data-status') == 1) {
    //         $(this).removeClass('selected');
    //         $(this).attr('data-status', 0);
    //         mediaArray.splice(mediaArray.indexOf($(this), 1));
    //         $message.html('Remove');
    //
    //     }
    // });
});
