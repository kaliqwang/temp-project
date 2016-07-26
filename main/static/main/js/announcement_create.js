$(document).ready(function() {
    // Templates
    var $imageFileTemplate = $('#image-file-template').html().trim();
    var $imageLinkTemplate = $('#image-link-template').html().trim();
    var $videoTemplate = $('#youtube-video-template').html();
    Mustache.parse($imageFileTemplate);
    Mustache.parse($imageLinkTemplate);
    Mustache.parse($videoTemplate);

    // Variables
    var $imageFilesAdd = $('#image-files-add');
    var $imageFilesClear = $('#image-files-clear');
    var $imageFilesPreview = $('#image-files-preview');
    var $imageFilesFilenames = $('#image-files-filenames');

    var $imageFilesBadge = $imageFilesAdd.siblings().find('span.badge');
    var $imageFilesCount = $imageFilesBadge.find('.count');
    var $imageFilesLoading = $imageFilesBadge.find('.glyphicon-refresh');
    var $imageFilesOk = $imageFilesBadge.find('.glyphicon-ok');

    var filenames = '';
    var processedCount = 0;
    var totalCount = 0;

    var $imageLinksAdd = $('#image-links-add');
    var $imageLinksPreview = $('#image-links-preview');
    var $imageTester = $('#image-tester');

    var $youTubeVideosAdd = $('#youtube-videos-add');
    var $youTubeVideosPreview = $('#youtube-videos-preview');

    /****************************** Image Files *******************************/

    $imageFilesAdd.on('change', function(){
        $imageFilesLoading.show(0);
        $imageFilesOk.hide(0);
        $imageFilesPreview.html('');
        $imageFilesClear.addClass('hidden');
        var files = $(this)[0].files;
        totalCount = files.length;
        jQuery.each(files, function(i, file){
            var imageReader = new FileReader();
            imageReader.onload = function(e){
                var path = e.target.result;
                $imageFilesPreview.prepend(Mustache.render($imageFileTemplate, {
                  imageURL: path,
                }));
                updateFilenames(file, path);
            }
            imageReader.readAsDataURL(file);
        });
    });

    $imageFilesClear.on('click', function() {
        $imageFilesBadge.addClass('hidden');
        $imageFilesFilenames.html('');
        $imageFilesPreview.html('');
        $imageFilesClear.addClass('hidden');
        var filenames = '';
        var processedCount = 0;
        var totalCount = 0;
        $imageFilesAdd.wrap('<form>').closest('form')[0].reset();
        $imageFilesAdd.unwrap();
    });

    function updateFilenames(file, path) {
        processedCount++;
        $imageFilesCount.html(processedCount);
        $imageFilesBadge.removeClass('hidden');
        filenames += '<a href="' + path + '" class="no-underline" target="_blank"><span class="label label-default">' + file.name + ' (' + bytesToSize(file.size) + ')</span></a> ';
        $imageFilesFilenames.html(filenames + '<br /><br />');
        if (processedCount == totalCount) {
            $imageFilesLoading.hide(0);
            $imageFilesOk.show(0);
            filenames = '';
            processedCount = 0;
            totalCount = 0;
            $imageFilesClear.removeClass('hidden');
        }
    }

    /****************************** Image Links *******************************/

    $imageLinksAdd.on('change', function(){
        var path = $(this).val();
        $imageTester.attr('src', path);
    }).on('paste', function(e){
        var path = e.originalEvent.clipboardData.getData('text');
        $imageTester.attr('src', path);
    });

    $imageTester.load(function(){
        $imageLinksAdd.val('');
        $imageLinksAdd.parent().removeClass('has-error');
        $imageLinksAdd.siblings('span').addClass('hidden');
        var path = $(this).attr('src');
        $imageLinksPreview.prepend(Mustache.render($imageLinkTemplate, {
          imageURL: path,
        }));
    }).error(function(){
        if ($(this).data('status') == 0){
            $(this).data('status', 1);
        } else {
            $imageLinksAdd.parent().addClass('has-error');
            $imageLinksAdd.siblings('span').removeClass('hidden');
        }
  	});

    /***************************** YouTube Videos *****************************/

    $youTubeVideosAdd.on('change', function(){
        var videoID = $(this).val().split('v=')[1];
        addYouTubeVideo(videoID, $youTubeVideosPreview);
    }).on('paste', function(e){
        var videoID = e.originalEvent.clipboardData.getData('text').split('v=')[1];
        addYouTubeVideo(videoID, $youTubeVideosPreview);
    });

    function addYouTubeVideo(videoID, $container) {
        $.ajax({
            type: 'GET',
            url: '../../../ytdata/' + videoID,
            success: function(data){
                $youTubeVideosAdd.val('');
                $youTubeVideosAdd.parent().removeClass('has-error');
                $youTubeVideosAdd.siblings('span').addClass('hidden');
                $container.prepend(Mustache.render($videoTemplate, {
                    thumbnailURL: 'http://img.youtube.com/vi/' + videoID + '/mqdefault.jpg',
                    videoTitle: data.title,
                    videoAuthor: data.author_name,
                    videoAuthorURL: data.author_url,
                    videoID: videoID,
                }));
            },
            error: function() {
                $youTubeVideosAdd.parent().addClass('has-error');
                $youTubeVideosAdd.siblings('span').removeClass('hidden');
            }
        });
    }

    /**************************** Helper Functions ****************************/

    function bytesToSize(bytes) {
        var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
        if (bytes == 0) return '0 Bytes';
        var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
        return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
    }
});
