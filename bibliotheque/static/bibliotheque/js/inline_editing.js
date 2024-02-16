const inline_textarea_false_statement = {
  selector: '.inline_textarea_false_statement',
  menubar: false,
  inline: true,
  plugins: [
    'link',
    'lists',
    'autolink',
    'code'
  ],

  toolbar: [
    'undo redo | bold italic underline | fontfamily fontsize',
    'forecolor backcolor | alignleft aligncenter alignright alignfull | numlist bullist outdent indent | code'
  ],

  valid_elements: 'p[style], strong, em, span[style], a[href], ul, ol, li',

  valid_styles: {
    '*': 'font-size,font-family,color,text-decoration,text-align'
  },
  powerpaste_word_import: 'clean',
  powerpaste_html_import: 'clean',
};

tinymce.init(inline_textarea_false_statement);

$(document).ready(function(){
    // get info on select

    $(".edit_note").click(function() {
        //requete_section_id = this.id ;
        var requete_section_id = $(this).parent().attr('id');
        console.log(requete_section_id);

        $('#' + requete_section_id ).focusout(function(){
            var myContent = {requete_section_id: requete_section_id,
                             requete_item_text: tinymce.get(requete_section_id).getContent(),
                             csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
                        };
            //console.log(myContent);
//            $.ajax({
//                method:"POST",
//                url: "http://127.0.0.1:8000/bibliotheque/text/update/",
//                dataType: "json",
//                //data:'etatdelasituation='+myContent,
//                data:myContent,
//                    success: function(data){
//                        console.log(data);
//                    },
//
//            });
        });
    });
});