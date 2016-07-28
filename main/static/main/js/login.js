$(document).ready(function() {
    var userAuthenticated = $('#user-authentication').text();
    if (userAuthenticated == 'False') {
        $('#login-modal').modal('show');
    }
});
