

$( document ).ready(function() {
    console.log( "ready!" );
    var timelineId = $( ".timelinejs-container" ).attr('id')
    console.log( timelineId );
    var URL = 'http://127.0.0.1:8000/timelinejs/data/json/' + timelineId
    console.log( URL );
    $.get(URL,function(data, status) {
        var options = {
            hash_bookmark: false,
            height: 10,
            scale_factor:1,
            initial_zoom: 1,
            zoom_sequence: [0.5, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

        }
        timeline = new TL.Timeline('timeline-embed', data, options);
    });
});
