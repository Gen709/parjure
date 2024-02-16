$(document).ready(function() {
    // $('input[name="headline"], textarea[name="text"]').focus(function() {
    //   // Get initial values
    // //   console.log("Entire structure:", $(this).closest('.row').html());
    //   var initialPictureId = $(this).closest('.image_row').find('input[name="picture_id"]').val();
    //   var initialPictureSource = $(this).closest('.row').find('input[name="picture_source"]').val();

    //   // Do something when the input comes into focus
      
      
    // });

    $('input[name="headline"], textarea[name="text"]').blur(function() {
      // Get the updated value
      var updatedValue = $(this).val();
      var inputName = $(this).attr('name');

      // Get initial values
      var initialPictureId = $(this).closest('.image_row').find('input[name="picture_id"]').val();
      
      console.log("Input blured", 'initialPictureId', initialPictureId, 'name', inputName);

      // Make an AJAX call to update the model
      $.ajax({
        type: 'POST',
        url: 'flikr/update/',  // Replace with your Django view URL
        data: {
          picture_id: initialPictureId,
          updated_value: updatedValue,
          inputName: inputName,
          csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()  // Include CSRF token
        },
        success: function(response) {
          // Handle success response
        //   /console.log(response);
    
        },
        error: function(error) {
          // Handle error
          console.error(error);
        }
      });

      // Do something when the input goes out of focus
      console.log("Input blurred");
    });
  });