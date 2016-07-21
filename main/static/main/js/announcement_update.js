$(document).ready(function() {

    // YouTube videos
    var context;

    var $youTubeExisting = $('#youtube-videos-existing');
    var $youTubePreview = $('#youtube-videos-preview');
    var youTubeTemplate = $('#youtube-video-template').html();
    Mustache.parse(youTubeTemplate);

    $('#youtube-videos-add').on('paste', function(e){
        console.log('EVENT DETECTED: <Paste>');
        var videoID = e.originalEvent.clipboardData.getData('text');
        addYouTubeVideo(videoID);
    }).on('change', function(){
        console.log('EVENT DETECTED: <Change>');
        var videoID = $(this).val();
        addYouTubeVideo(videoID);
    });

    $('#youtube-videos-existing').children('.hidden').each(function(){
        var videoID = $(this).text();
        addExistingYouTubeVideo(videoID);
    });

    function addYouTubeVideo(id) {
        $.ajax({
            type: 'GET',
            url: '../../../ytdata/' + id,
            dataType: 'json',
            success: function(data){
                console.log('Success: video found');
                context = {
                    videoID: id,
                    thumbnailURL: 'http://img.youtube.com/vi/' + id + '/mqdefault.jpg',
                    videoTitle: data.title,
                    videoAuthor: data.author_name,
                    videoAurthorURL: data.author_url
                };
                $youTubePreview.prepend(Mustache.render(youTubeTemplate, context));
                $('#youtube-videos-add').val('');
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log('Error: no video found');
            }
        });
    }

    function addExistingYouTubeVideo(id) {
        $.ajax({
            type: 'GET',
            url: '../../../ytdata/' + id,
            dataType: 'json',
            success: function(data){
                console.log('Success: video found');
                context = {
                    videoID: id,
                    thumbnailURL: 'http://img.youtube.com/vi/' + id + '/mqdefault.jpg',
                    videoTitle: data.title,
                    videoAuthor: data.author_name,
                    videoAurthorURL: data.author_url
                };
                $youTubeExisting.append(Mustache.render(youTubeTemplate, context));
            },
            error: function(xhr, textStatus, errorThrown) {
                console.log('Error: no video found');
            }
        });
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
        var e = Mustache.render(imageLinkTemplate, {imageURL: link});
        $(e).prependTo($imageLinksPreview).find('.nailthumb-container > img').load(function(){
            $(this).parent().nailthumb({preload:false, replaceAnimation:null}).removeClass('hidden');
        });
        $('#image-links-add').val('');
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

    // Submit Form
    $('#submit-announcement-update-form').click(function(e){
        e.preventDefault();
        var error = false;
        if(!$('#announcement-update-form')[0].checkValidity()) {
            $('input.form-control, textarea.form-control').each(function() {
                if ($(this).val().trim() == '') {
                    $(this).parent().addClass('has-error');
                    $(this).siblings().children().css('border-color', '#a94442');
                    error = true;
                } else {
                    $(this).parent().removeClass('has-error');
                    $(this).siblings().children().css('border-color', '#ccc');
                }
            });
        }
        if (!error) {
            $('#image-links-add').remove();
            $('#youtube-videos-add').remove();
            $('#image-links-existing').remove();
            $('#youtube-videos-existing').remove();
            $('#announcement-update-form').submit();
        }
    });
});
