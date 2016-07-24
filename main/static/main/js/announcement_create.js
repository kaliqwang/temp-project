$(document).ready(function() {

    // YouTube videos
    var context;

    var $youTubeVideosAdd = $('#youtube-videos-add');
    var $youTubePreview = $('#youtube-videos-preview');
    var youTubeTemplate = $('#youtube-video-template').html();
    Mustache.parse(youTubeTemplate);

    $youTubeVideosAdd.on('paste', function(e){
        console.log('EVENT DETECTED: <Paste>');
        var videoURL = e.originalEvent.clipboardData.getData('text');
        var videoID = parseYouTubeURL(videoURL);
        addYouTubeVideo(videoID);
    }).on('change', function(){
        console.log('EVENT DETECTED: <Change>');
        var videoURL = $(this).val();
        var videoID = parseYouTubeURL(videoURL);
        addYouTubeVideo(videoID);
    });

    function addYouTubeVideo(id) {
        $.ajax({
            type: 'GET',
            url: '../../ytdata/' + id,
            crossOrigin: true,
            success: function(data){
                $youTubeVideosAdd.parent().removeClass('has-error');
                console.log('Success: video found');
                context = {
                    videoID: id,
                    thumbnailURL: 'http://img.youtube.com/vi/' + id + '/mqdefault.jpg',
                    videoTitle: data.title,
                    videoAuthor: data.author_name,
                    videoAuthorURL: data.author_url,
                };
                $youTubePreview.prepend(Mustache.render(youTubeTemplate, context));
                $('#youtube-videos-add').val('');
            },
            error: function(xhr, textStatus, errorThrown) {
                $youTubeVideosAdd.parent().addClass('has-error');
                console.log('Error: no video found');
            }
        });
    }

    function parseYouTubeURL(url) {
        return url.split('v=')[1];
    }

    // Image links

    var $imageLinksAdd = $('#image-links-add');
    var $imageTester = $('#image-tester');
    var $imageLinksPreview = $('#image-links-preview');
    var imageLinkTemplate = $('#image-link-template').html();
    Mustache.parse(imageLinkTemplate);

    $imageLinksAdd.on('paste', function(e){
        console.log('EVENT DETECTED: <Paste>');
        var link = e.originalEvent.clipboardData.getData('text');
        $imageTester.attr('src', link);
    }).on('change', function(){
        console.log('EVENT DETECTED: <Change>');
        var link = $(this).val();
        $imageTester.attr('src', link);
    });

    $imageTester.load(function(){
        $imageLinksAdd.parent().removeClass('has-error');
        console.log('Success: image loaded');
        addImageLink($(this).attr('src'));
    }).error(function(){
        $imageLinksAdd.parent().addClass('has-error');
  		  console.log('Error: invalid image url');
  	});

    function addImageLink(link) {
        var e = Mustache.render(imageLinkTemplate, {imageURL: link});
        $(e).prependTo($imageLinksPreview).find('.nailthumb-container > img').load(function(){
            $(this).parent().nailthumb({preload:false, replaceAnimation:null}).removeClass('hidden');
        });
        $imageLinksAdd.val('');
    }

    // Image files

    var $imageFilesPreview = $('#image-files-preview');
    var imageFileTemplate = $('#image-file-template').html();
    Mustache.parse(imageFileTemplate);

    $('#image-files-add').on('change', function(e){
        var files = e.target.files;
        $imageFilesPreview.html('');
        jQuery.each(files, function(i, file){
            imageFilePreview(file);
        });
    });

    function imageFilePreview(f) {
        var imageReader = new FileReader();
        imageReader.onload = function(e){
            var link = e.target.result;
            var e = Mustache.render(imageFileTemplate, {imageURL: link});
            $(e).prependTo($imageFilesPreview).find('.nailthumb-container > img').load(function(){
                $(this).parent().nailthumb({preload:false, replaceAnimation:null}).removeClass('hidden');
            });
        }
        imageReader.readAsDataURL(f);
    }
});
