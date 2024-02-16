
$( document ).ready(function() {
//    get all the timeline's id and div id and loop
    $('.timeline').each(function(index, value) {
        var test = this.id.split("_");
        var timeline_id = test[1]
        var URL = 'http://127.0.0.1:8000/timelinejs/data/json/' + timeline_id

        $.get(URL,function(data, status) {
            var options = {
                hash_bookmark: false,
                height: 10,
                scale_factor:1,
                initial_zoom: 1,
                zoom_sequence: [0.5, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

            }
            timeline = new TL.Timeline('timeline_' + timeline_id, data, options);
        });

    });

});