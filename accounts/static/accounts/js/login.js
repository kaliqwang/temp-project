$(document).ready(function() {
    var userAuthenticated = $('#user-authentication').text();
    if (userAuthenticated == 'False') {
        $('#login-modal').modal('show');
    }
});

$('#login-modal').keypress(function(e) {
    if (e.which == 13) {
        $('#login-form').submit();
        return false;
    }
});
