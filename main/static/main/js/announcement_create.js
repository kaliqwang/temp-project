$(document).ready(function() {

    // YouTube videos

    var $youTubePreview = $('#youtube-videos-preview');
    var youTubeTemplate = $('#youtube-video-template').html();
    Mustache.parse(youTubeTemplate);

    $('#youtube-videos-add').on('paste', function(e){
        console.log('EVENT DETECTED: <Paste>');
        var video = e.originalEvent.clipboardData.getData('text');
        checkVideoID(video);
    }).on('change', function(){
        console.log('EVENT DETECTED: <Change>');
        var video = $(this).val();
        checkVideoID(video);
    });

    function checkVideoID(id) {
        var videoID = id;
        $.ajax({
            type: 'GET',
            url: '../../ytdata/' + videoID,
            dataType: 'json',
            success: function(data){
                console.log('Success: video found');
                addYouTubeVideo(data, videoID);
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log('Error: no video found');
            }
        });
    }

    function addYouTubeVideo(data, id) {
        var context = {
            videoID: id,
            thumbnailURL: 'http://img.youtube.com/vi/' + id + '/mqdefault.jpg',
            videoTitle: data.title,
            videoAuthor: data.author_name,
            videoAurthorURL: data.author_url
        };
        $youTubePreview.append(Mustache.render(youTubeTemplate, context));
        $('#youtube-videos-add').val('');
    }

    // Image links

    var $imageLinksPreview = $('#image-links-preview');
    var imageLinkTemplate = $('#image-link-template').html();
    Mustache.parse(imageLinkTemplate);

    $('#image-links-add').on('paste', function(e){
        console.log('EVENT DETECTED: <Paste>');
        var link = e.originalEvent.clipboardData.getData('text');
        $('#image-tester').attr('src', link);
    }).on('change', function(){
        console.log('EVENT DETECTED: <Change>');
        var link = $(this).val();
        $('#image-tester').attr('src', link);
    });

    $('#image-tester').load(function(){
        console.log('Success: image loaded');
        addImageLink($(this).attr('src'));
    }).error(function(){
  		  console.log('Error: invalid image url');
  	});

    function addImageLink(link) {
        $imageLinksPreview.append(Mustache.render(imageLinkTemplate, {imageURL: link}));
        $('#image-links-add').val('');
    }

    // Image files

    var $imageFilesPreview = $('#image-files-preview');

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
            $imageFilesPreview.append('<img class="thumbnail-preview" src="' + e.target.result + '">');
        }
        imageReader.readAsDataURL(f);
    }
});
