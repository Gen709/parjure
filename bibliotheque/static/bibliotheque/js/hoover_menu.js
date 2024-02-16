// https://stackoverflow.com/questions/65294022/bootstrap-v5-how-to-pass-a-variable-inside-a-modal-without-jquery
// http://kenwheeler.github.io/slick/

function appendTextToModalOnClick(false_statement_id) {
    // this is not the parent id but the element to edit
    // this is to edit comment should not be available to edit the allegations
    var myContent={parent_id: false_statement_id};

    $.ajax({
		method:"POST",
		url: "http://127.0.0.1:8000/bibliotheque/requete/text/get/",
		dataType: "json",
		data:myContent,
        success: function(data) {

            var false_statement_title = data[0]["title"];
            var false_statement_text = data[0]["text"];
            var desc = data[0]["desc"];
            var parent = data[0]["parent"];
            var lft = data[0]["lft"];
            var rgt = data[0]["rgt"];
            var section_id = data[0]["section_id"];
            var modalContainer = document.getElementById('editFalseAllegationModal');

            if (desc == 1) {
//                only need the item as text no title
                html_str = `<div class="row border rounded mt-4">
                                <input type="hidden" name="section" value="` + section_id + `" id="section_id">
                                <input type="hidden" name="parent" value="` + parent + `" id="id_parent">
                                <input type="hidden" name="lft" value="` + lft + `" id="id_lft">
                                <input type="hidden" name="rgt" value="` + rgt + `" id="id_rgt">
                                <div class="mb-3">
                                    <label class="form-label" for="id_item">
                                        Item
                                    </label>
                                    <textarea name="item" cols="40" rows="4" class="false_statement_text form-control" placeholder="Item" title="" required id="id_item">`+false_statement_title+`
                                    </textarea>
                                </div>
                                <input type="hidden" name="text" value="None" id="id_text">
                                <input type="hidden" name="desc" value="1" value="requete" id="id_desc">
                                <input type="hidden" name="is_true" value="False" id="id_is_true">
                            </div>`;

            } else if (desc == 2) {
                html_str = `<div class="row border rounded mt-4">
                                <input type="hidden" name="section" value="` + section_id + `" id="section_id">
                                <input type="hidden" name="parent" value="` + parent + `" id="id_parent">
                                <input type="hidden" name="lft" value="` + lft + `" id="id_lft">
                                <input type="hidden" name="rgt" value="` + rgt + `" id="id_rgt">
                                <div class="mb-3">
                                    <label class="form-label" for="id_item">
                                        Allégation reliée
                                    </label>
                                    <div class="row mt-2"><p><strong>`+ false_statement_title + `</p></strong></div>
                                </div>
                                <div class="mb-3">
                                    
                                    <textarea name="item" cols="40" rows="6" placeholder="Détails" class="false_statement_text form-control" title="" id="id_item">`+ false_statement_text +`
                                    </textarea>
                                </div>
                                <input type="hidden" name="desc" value="2" value="explication" id="id_desc">
                                <input type="hidden" name="is_true" value="None" id="id_is_true">
                            </div>`;
            };


            modalContainer.querySelector(".inline_textarea_explanation").innerHTML = html_str

            const inline_textarea_update = {
                selector: '.false_statement_text',
                height: "360",
                entity_encoding : "raw",
                menubar: true,
                inline: false,
                plugins: ['link', 'lists', 'autolink', 'code', 'image' ],

                toolbar: [
                    'undo redo | bold italic underline | fontfamily fontsize',
                    'forecolor backcolor | alignleft aligncenter alignright alignfull | numlist bullist outdent indent | code'
                ]

            };

            tinymce.init(inline_textarea_update);

            // Prevent bootstrap dialog from blocking focusin
            document.addEventListener('focusin', function(e) {
                if (e.target.closest(".tox-tinymce-aux, .moxman-window, .tam-assetmanager-root") !== null) {
                    e.stopImmediatePropagation();
                }
            });
        },

    });

};


function modalAddChild(parent_id, action_type) {

    var modalContainer = document.getElementById('addChild');
    
    console.log(action_type);
    if (action_type == 'as_child') {
        var anchorSelector = '#'+ parent_id + ' .false-statements .col a';
        var modalWindowTitle = 'Insérer comme enfants';
      } else if(action_type =='as_sibbling'){
        var anchorSelector = '#' + parent_id + '.row.rebuttal .col.item.border.rounded';
        var modalWindowTitle = 'Insérer comme fraterie';
      } else if(action_type == 'edit_text' ){
        var anchorSelector = '#' + parent_id + '.row.rebuttal .col.item.border.rounded';
        var modalWindowTitle = 'Modifier le text';
      }
    
    var modalTitle = modalContainer.querySelector('.modal-title');
    modalTitle.textContent = modalWindowTitle;

    // var allegation = $(anchorSelector).text();
    var allegation = $(anchorSelector).html();
    console.log("anchorSelector", anchorSelector, "allegation", allegation)

    if (action_type == 'as_child') {
        modalContainer.querySelector(".statement-to-comment").innerHTML = allegation;
      } else if(action_type == 'edit_text' ){
        modalContainer.querySelector(".inline_textarea_explanation").innerHTML = allegation;
      }

    var hiddenInputParentId = modalContainer.querySelector("input[name='parent_id']");
    hiddenInputParentId.value = parent_id;

    var hiddenInputAction = modalContainer.querySelector("input[name='action_type']");
    hiddenInputAction.value = action_type;


    $.ajax({
        url: '/get_image_list/',
        type: 'GET',
        success: function (data) {
            // Update TinyMCE configuration with the fetched image data
            tinymce.init({
                selector: '.inline_textarea_explanation',
                entity_encoding : "raw",
                height: "360",
                menubar: true,
                inline: false,
                plugins: ['link', 'lists', 'autolink', 'code', 'image' ],

                toolbar: [
                'undo redo | bold italic underline | fontfamily fontsize',
                'forecolor backcolor | alignleft aligncenter alignright alignfull | numlist bullist outdent indent | code'
                ],
                image_list: data,
            });
        },
        error: function (error) {
            console.error('Error fetching image data:', error);
        }
    });

    document.addEventListener('focusin', function(e) {
        if (e.target.closest(".tox-tinymce-aux, .moxman-window, .tam-assetmanager-root") !== null) {
            e.stopImmediatePropagation();
        }
    });

};


function modalAddComment(parent_id, rgt, lft, desc) {
    
    var parent_text = $("#"+parent_id).children(".false-statement").children('a').text();
    console.log("id", parent_id, "text", parent_text)
//    aller cherlcher le txt dans la bd
    var modalContainer = document.getElementById('addExplainationeModal');
    modalContainer.querySelector(".statement-to-comment").innerHTML = `<p>` + parent_text + `</p>`;

//    attribut le id du parent à l'element du formulaire
    $('input[name="parent_id"]').attr("value", parent_id);
    $('input[name="parent"]').attr("value", parent_id);

    if (desc == 1) {
        $('input[name="lft"]').attr("value", lft + 1);
        $('input[name="rgt"]').attr("value", lft + 2);
    } else if (desc == 2) {
        $('input[name="lft"]').attr("value", rgt + 1);
        $('input[name="rgt"]').attr("value", rgt + 2);
    };


    $('input[name="document_section"]').attr("value", parent_id);


    const inline_textarea_explanation = {
        selector: '.inline_textarea_explanation',
        entity_encoding : "raw",
        height: "360",
        menubar: true,
        inline: false,
        plugins: ['link', 'lists', 'autolink', 'code', 'image' ],

        toolbar: [
        'undo redo | bold italic underline | fontfamily fontsize',
        'forecolor backcolor | alignleft aligncenter alignright alignfull | numlist bullist outdent indent | code'
        ]

    };

    tinymce.init( inline_textarea_explanation );

    // Prevent bootstrap dialog from blocking focusin
    document.addEventListener('focusin', function(e) {
        if (e.target.closest(".tox-tinymce-aux, .moxman-window, .tam-assetmanager-root") !== null) {
            e.stopImmediatePropagation();
        }
    });

};


function modalAddCommentAsSibling(parent_id, rgt, lft, desc) {
    var parent_text = $("#"+parent_id).children(".false-statement").children('a').text();
//    aller cherlcher le txt dans la bd

    var modalContainer = document.getElementById('addExplainationeModal');
    modalContainer.querySelector(".statement-to-comment").innerHTML = `<p>` + parent_text + `</p>`;

//    attribut le id du parent à l'element du formulaire
    $('input[name="parent_id"]').attr("value", parent_id);
    $('input[name="parent"]').attr("value", parent_id);

    if (desc == 1) {
        $('input[name="lft"]').attr("value", lft + 1);
        $('input[name="rgt"]').attr("value", lft + 2);
    } else if (desc == 2) {
        $('input[name="lft"]').attr("value", rgt + 1);
        $('input[name="rgt"]').attr("value", rgt + 2);
    };


    $('input[name="document_section"]').attr("value", parent_id);


    const inline_textarea_explanation = {
        selector: '.inline_textarea_explanation',
        entity_encoding : "raw",
        height: "360",
        menubar: true,
        inline: false,
        plugins: ['link', 'lists', 'autolink', 'code', 'image' ],

        toolbar: [
        'undo redo | bold italic underline | fontfamily fontsize',
        'forecolor backcolor | alignleft aligncenter alignright alignfull | numlist bullist outdent indent | code'
        ]

    };

    tinymce.init( inline_textarea_explanation );

        // Prevent bootstrap dialog from blocking focusin
    document.addEventListener('focusin', function(e) {
        if (e.target.closest(".tox-tinymce-aux, .moxman-window, .tam-assetmanager-root") !== null) {
            e.stopImmediatePropagation();
        }
    });

};


function AddAllegationModalOnClick(sibling_id) {

    var URL = 'http://127.0.0.1:8000/bibliotheque/documentitem/data/json/';

    $.ajax({
            method:"POST",
            url: URL,
            dataType: "json",
            //data:'etatdelasituation='+myContent,
            data:{'sibling_id': sibling_id},
            success: function(data){
                console.log(data);
                $("#id_parent").val(data["id_parent"]);
                $("#id_lft").val(data["id_lft"]);
                $("#id_rgt").val(data["id_rgt"]);

            },
		});

    textarea_name="item";
};


function AddParentIdToTimelineModal(related_id){
    var URL = 'http://127.0.0.1:8000/bibliotheque/documentitem/data/json/';

    $.ajax({
            method:"POST",
            url: URL,
            dataType: "json",
            //data:'etatdelasituation='+myContent,
            data:{'sibling_id': related_id},
            success: function(data){
                console.log(data);
                $("input[name='timeline_related_item']").val(data["id_parent"]);

                var modalContainer = document.getElementById('addTimelineModal');
                modalContainer.querySelector("#timeline-related-item").innerHTML = `<p>` + data["item"] + `</p>`;


            },
		});
};


function addAsChild(parent_id, rgt, lft, desc) {
    document.getElementById('main_form').setAttribute("action", 'http://127.0.0.1:8000/bibliotheque/add/child/');
    var myContent={parent_id: parent_id};
    var title_section = document.getElementById('editFalseAllegationModalLabel');
    title_section.innerHTML = "Add rebuttal element as child";

    $.ajax({
		method:"POST",
		url: "http://127.0.0.1:8000/bibliotheque/requete/text/get/",
		dataType: "json",
		data:myContent,
        success: function(data) {

            var desc = data[0]["desc"];
            var parent_id = data[0]["parent"];
            var lft = data[0]["lft"] + 1;
            var rgt = data[0]["lft"] + 2;

            var modalContainer = document.getElementById('editFalseAllegationModal');

            html_str = `<div class="row border rounded mt-4">
                                <input type="hidden" name="parent" value="` + parent_id + `" id="id_parent">
                                <input type="hidden" name="lft" value="` + lft + `" id="id_lft">
                                <input type="hidden" name="rgt" value="` + rgt + `" id="id_rgt">
                                <div class="mb-3">
                                    <label class="form-label" for="id_item">
                                        Détails de la section
                                    </label>
                                    <textarea name="item" cols="40" rows="1" placeholder="Titre de la section" class="form-control" title="" required id="id_item"></textarea>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label" for="id_text">
                                        Text
                                    </label>
                                    <textarea name="text" cols="40" rows="6" placeholder="Détails" class="false_statement_text form-control" title="" id="id_text"></textarea>
                                </div>
                                <input type="hidden" name="desc" value="2" value="explication" id="id_desc">
                                <input type="hidden" name="is_true" value="None" id="id_is_true">
                            </div>`;

            modalContainer.querySelector(".inline_textarea_explanation").innerHTML = html_str
        }
    });
};


function addAsSibling( sibling_id, rgt, lft, desc ) {
    document.getElementById('main_form').setAttribute("action", 'http://127.0.0.1:8000/bibliotheque/add/siblings/');
    var title_section = document.getElementById('editFalseAllegationModalLabel');
    var new_lft = rgt + 1;
    var new_rgt = rgt + 2;

    title_section.innerHTML = "Add rebuttal element as sibling";

    var modalContainer = document.getElementById('editFalseAllegationModal');

    if (desc == 1) {
        html_str = `<div class="row border rounded mt-4">
                    <input type="hidden" name="parent" value="` + sibling_id + `"id="id_parent">
                    <input type="hidden" name="lft" value="` + new_lft + `" id="id_lft">
                    <input type="hidden" name="rgt" value="` + new_rgt + `" id="id_rgt">
                    <div class="mb-3">
                        <label class="form-label" for="id_item">
                            Allegation
                        </label>
                        <textarea name="item" cols="40" rows="1" placeholder="Titre de la section" class="form-control" title="" required id="id_item"></textarea>
                    </div>
                    <input type="hidden" name="text" value="" id="id_text">
                    <input type="hidden" name="desc" value="` + desc + `" value="explication" id="id_desc">
                    <input type="hidden" name="is_true" value="None" id="id_is_true">
                </div>`;
        
    } else if (desc == 2) {
        html_str = `<div class="row border rounded mt-4">
                    <input type="hidden" name="parent" value="` + sibling_id + `"id="id_parent">
                    <input type="hidden" name="lft" value="` + new_lft + `" id="id_lft">
                    <input type="hidden" name="rgt" value="` + new_rgt + `" id="id_rgt">
                    <div class="mb-3">
                        <label class="form-label" for="id_item">
                            Détails de la section
                        </label>
                        <textarea name="item" cols="40" rows="1" placeholder="Titre de la section" class="form-control" title="" required id="id_item"></textarea>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" for="id_text">
                            Text
                        </label>
                        <textarea name="text" cols="40" rows="6" placeholder="Détails" class="false_statement_text form-control" title="" id="id_text"></textarea>
                    </div>
                    <input type="hidden" name="desc" value="` + desc + `" value="explication" id="id_desc">
                    <input type="hidden" name="is_true" value="None" id="id_is_true">
                </div>`;
    };

    

    modalContainer.querySelector(".inline_textarea_explanation").innerHTML = html_str;

};


$(document).ready(function(){

    $(".rebuttal").mouseenter(function() {

        // Get the ID attribute value of the found ancestor
        var rebutal_id = $(this).attr('id');
        var anchorSelector = '#' + rebutal_id + '.row.rebuttal .col.item.border.rounded';
        var allegation = $(anchorSelector).html();
        console.log("rebutal id:", rebutal_id, 'allegation', allegation);

        var htm_menu_depth_1 = `<div class="row row-menu justify-content-end mt-3">
                                    <div class="col-sm-1">  
                                        <span class="material-symbols-outlined d-flex justify-content-center align-items-center">
                                            <a  class="menu-link edit_note" type="button" data-bs-toggle="modal" data-bs-target="#addChild" onClick="modalAddChild(` + rebutal_id + `, 'as_sibbling' )" data-toggle="tooltip" data-placement="top" title="Ajouter une exlication">
                                                person_add
                                            </a>
                                        </span>
                                    </div>
                                    <div class="col-sm-1"> 
                                        <span class="material-symbols-outlined d-flex justify-content-center align-items-center">
                                            <a  class="menu-link edit_note" type="button" data-bs-toggle="modal" data-bs-target="#addChild" onClick="modalAddChild(` + rebutal_id + `, 'edit_text' )" data-toggle="tooltip" data-placement="top" title="Modifier l'exlication">
                                                edit_note
                                            </a>
                                        </span>
                                    </div>
                                    <div class="col-sm-1">
                                        <span class="material-symbols-outlined d-flex justify-content-center align-items-center">
                                            <a  href="http://127.0.0.1:8000/leaf/delete/`+ rebutal_id +`" data-toggle="tooltip" data-placement="top" title="Suprimer l'explication">
                                                delete
                                            </a>
                                        </span>
                                    </div>
                                    <div class="col-sm-1">
                                    </div>
                                    <div class="col-sm-1">
                                    </div>
                                    <div class="col-sm-1"> 
                                    </div>
                                    <div class="col-sm-1">  
                                    </div>
                                </div>`

       

        $(this).children("div.menu-box").append(htm_menu_depth_1);
        
    })
    .mouseleave(function() {
        $(this).children("div.menu-box").children("div.row-menu").remove();
    });



    $(".false-statements").mouseenter(function() {

        var statementRowElement = $(this).closest('.row.statement');

        var false_statement_id = statementRowElement ? statementRowElement.attr('id') : null;

        var lft = document.getElementById(false_statement_id + '_lft').getAttribute('data-lft');
        var rgt = document.getElementById(false_statement_id + '_rgt').getAttribute('data-rgt');
        var desc = document.getElementById(false_statement_id + '_desc').getAttribute('data-desc');
        var depth = document.getElementById(false_statement_id + '_depth').getAttribute('data-depth');
        
        var htm_menu_depth_1 = `<div class="row row-menu justify-content-end mt-3">
                                    <div class="col-sm-1">
                                        <span class="material-symbols-outlined d-flex justify-content-center align-items-center">
                                            <a  class="menu-link edit_note" type="button" data-bs-toggle="modal" data-bs-target="#addChild" onClick="modalAddChild(` + false_statement_id + `, 'as_child' )" data-toggle="tooltip" data-placement="top" title="Ajouter une exlication">
                                                add_circle
                                            </a>
                                        </span>
                                    </div>
                                    <div class="col-sm-1">  
                                    </div>
                                    <div class="col-sm-1">  
                                    </div>
                                    <div class="col-sm-1">
                                    </div>
                                    <div class="col-sm-1">
                                    </div>
                                    <div class="col-sm-1"> 
                                    </div>
                                    <div class="col-sm-1">  
                                    </div>
                                </div>`;

        $(this).children("div.menu-box").append(htm_menu_depth_1);  
    })
    .mouseleave(function() {
        $(this).children("div.menu-box").children("div.row-menu").remove();
    });

});



 