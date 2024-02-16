



function getPrevious(elemId) {
    if (elemId.prev("li").attr("id") === "undefined") {
        var elemParent =  elemId.parent().attr("id");
        var elemParentPreviousSibling = elemParent.prev("ol").attr("id");
    } else {
        return null;
    }
}

$(document).ready(function(){
    $( "ol#list_1 li" ).hover(
        function() {
            var previousSiblingId = $(this).prev("li").attr("id");
            var nextSiblingId = $(this).next("li").attr("id");
            var thisElementParent = $(this).parent();
            // thisElementParent.css( "background-color", "red" );
            var thisElementParentSibling = thisElementParent.prev("ol");
            $( this ).append( $( "<span> id --- (prev list id: " + thisElementParentSibling.attr("id") + "list id: " + thisElementParent.attr("id") + ") </span>" ) );
        }, function() {
          $( this ).find( "span" ).last().remove();
        //   $(this).parent().css( "background-color", "white" );
        }
      );
});