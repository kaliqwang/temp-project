$(document).ready(function() {
    // Variables
    $itemsDateTime = $('#announcement-list .signature .datetime');
    $itemsCollapse = $('#announcement-list .collapse');
    $toggleCollapseAll = $('#toggle-collapse-all');

    /****************************** On Page Load ******************************/

    // Remove periods from a.m. and p.m.
    $itemsDateTime.each(function(){
        var cleaned = $(this).text().replace(/\./g, '');
        $(this).text(cleaned);
        $(this).removeClass('hidden');
    });

    /***************************** Event Handlers *****************************/

    // Toggle text between "Show More" / "Show Less" (on collapse/hide)
    $itemsCollapse.on('show.bs.collapse', function(){
        $(this).siblings('.toggle-collapse').text('Show Less');
    }).on('hide.bs.collapse', function(){
        $(this).siblings('.toggle-collapse').text('Show More');
    });

    // Toggle collapse for all announcements (on click)
    $toggleCollapseAll.on('click', function(){
        if ($(this).data('mode') == '0') {
            $itemsCollapse.collapse('show');
            $(this).text('Collapse All');
            $(this).data('mode', 1);
        } else {
            $itemsCollapse.collapse('hide');
            $(this).text('Expand All');
            $(this).data('mode', 0);
        }
    });
});
