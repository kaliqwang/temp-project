var body = document.getElementsByTagName('body')[0];
var sidebar = document.getElementById('sidebar');

// sidebar overflow hide
sidebar.onmouseover = function() {
    body.style.overflow = 'hidden';
    body.style.margin = '0 15px 0 0';
}
sidebar.onmouseout = function() {
    body.style.overflow = 'auto';
    body.style.margin = '0 0 0 0';
}
