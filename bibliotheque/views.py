from django.shortcuts import render, redirect
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy, reverse

from django.views.decorators.csrf import csrf_exempt

from .models import DocumentItem, TypeDocument, DocumentText
from timelinejs.models import Events
from .forms import RequeteItemModelForm, CounterPointModelForm, DocumentItemForm

from django.http import JsonResponse
from flickr.models import Flickr
from photos.models import FlikrPhoto


from django.db import connection
# DocumentTextModelForm,


from django.http.response import JsonResponse, HttpResponse


def home(request):
    context = {}
    return render(request, "bibliotheque/home.html", context)


def get_full_tree(request, pk=2):
    document = DocumentItem.objects.get(id=pk)
    timelines = Events.objects.all()
    context = {"document": document,
               "timelines": timelines
               }
    return render(request, "bibliotheque/home.html", context)


def get_related(request, pk):
    allegation = DocumentItem.objects.get(id=pk)
    # child = DocumentItem.objects.filter()
    context = {"allegation": allegation}
    return render(request, 'bibliotheque/allegation_related.html', context)


@csrf_exempt
def text_get(request):
    #TODO: t is the element to edit, there is no text, the item is the text
    t = DocumentItem.objects.get(id=request.POST.get("parent_id"))
    parent = DocumentItem.objects.get(id=t.parent)
    data_list = [{'title': parent.item,
                  'text': t.item,
                  'desc': t.desc.id,
                  'parent': t.parent,
                  'lft': t.lft,
                  'rgt': t.rgt,
                  'section_id': t.id
                  }]
    data = JsonResponse(data_list, safe=False)
    mimetype = 'application/json'

    return HttpResponse(data, mimetype)


def text_update_old(request):
    if request.method == "POST":
        library_item_obj: DocumentItem = DocumentItem.objects.get(id=request.POST.get('section_id'))
        library_item_obj.item = request.POST.get('false_statement_title')
        library_item_obj.save()
        try:
            text = DocumentText.objects.get(document_section=library_item_obj)
            text.text = request.POST.get('false_statement_text')
            text.save()
        except:
            DocumentText.objects.create(document_section=library_item_obj, text=request.POST.get('false_statement_text'))



    return redirect('home')


def text_update(request, pk=None):
    if request.method == "POST":
        instance = DocumentItem.objects.get(id=int(request.POST.get('section')))
        form = DocumentItemForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save()
            return redirect('home')
        else:
            context = {'parent': instance.id,
                       'item_form': form
                       }
            return render(request, 'bibliotheque/counterpoint_item_text_form.html', context)
    else:
        element = DocumentItem.objects.get(id=pk)

        if element.desc.id == 1:
            form = RequeteItemModelForm(instance=element)
        elif element.desc.id == 2:
            form = CounterPointModelForm(instance=element)

        context = {'item_form': form,
                   'parent':element
                   }
        return render(request, 'bibliotheque/counterpoint_item_text_form.html', context)


def section_add(request):
    if request.method == "POST":
        relative = DocumentItem.objects.get(id=request.POST.get('parent_id'))
        if relative.desc.id == 1:
            # insert as item as child
            parameter = relative.lft
            parent_id = relative.id
        elif relative.desc.id == 2:
            # insert as sibbling
            parameter = relative.rgt
            parent_id =  relative.parent
        # parent_obj: DocumentItem = DocumentItem.objects.get(pk=parent_id)
        item = request.POST.get('explanation')

        form = RequeteItemModelForm({"parent": parent_id,
                                     "desc": TypeDocument.objects.get(id=2),
                                     "item": item,
                                     "lft": 1,
                                     "rgt": 2
                                     })
        if form.is_valid():
            new_item = form.save()
            # get parent
            parent_item = DocumentItem.objects.get(id=parent_id)
            # get parent left
            parent_left = parent_item.lft
            # get document item with lft element above parent left
            document_lft_qs = DocumentItem.objects.filter(lft__gt=parent_left)
            # update element
            for doc in document_lft_qs:
                doc.lft = doc.lft + 2
                doc.save()
            # get document item with rgt element above parent left
            document_rgt_qs = DocumentItem.objects.filter(rgt__gt=parent_left)
            for doc in document_rgt_qs:
                doc.rgt = doc.rgt + 2
                doc.save()
            new_item.lft = parent_left + 1
            new_item.rgt = parent_left + 2
            new_item.save()
            return redirect('home')


def add_as_child_old(request, parent_id=None):
    if request.method == "POST":
        form = CounterPointModelForm(request.POST)
        if form.is_valid():
            new_counterpoint = form.save()
            parent = DocumentItem.objects.get(id=request.POST.get('parent'))
            for x in DocumentItem.objects.filter(lft__gt=parent.lft):
                x.lft = x.left + 2
            for y in DocumentItem.objects.filter(rgt__gt=parent.lft):
                y.rgt = y.rgt + 2
            # new_counterpoint.lft = parent.lft + 1
            # new_counterpoint.rgt = parent.rgt + 2
            new_counterpoint.save()
            return redirect('home')



            return redirect('home')
        else:
            context = {'form', form}
            return render(request, '', context)

    else:
        parent = DocumentItem.objects.get(id=parent_id)
        context={}
        return render(request, '', context)


def add_as_child(request):
    if request.method == "POST":
        parent_id = request.POST.get("parent_id")
        action_type = request.POST.get("action_type")
        content = request.POST.get('mce_9')
        if action_type == "as_child":
            # query = 'CALL add_child_nod(' + str(parent_id) + ', "' + str(content) + '")'
            query = 'CALL add_child_nod(%s, %s)'
            params = (parent_id, str(content))
        elif action_type == 'as_sibbling':
            # query = 'CALL add_sibbling_nod(' + str(parent_id) + ', "' + str(content) + '")'
            query = 'CALL add_sibbling_nod( %s, %s)'
            params = (parent_id, str(content))
        elif action_type == 'edit_text':
            query = 'UPDATE bibliotheque_documentitem SET item = %s WHERE id = %s'
            params = (str(content), parent_id)
            
       
        print("query: ", query)
        with connection.cursor() as cursor:
                # add the children
                # cursor.execute(query)
                cursor.execute(query, params)
        return redirect(reverse("home"))
        
    else:
        
        return redirect(reverse("home"))


def deleting_leaf_node(request, pk):
    query = "CALL delete_leaf_nod("+ str(pk) + ")"
    print(query)
    with connection.cursor() as cursor:
        # add the children
        cursor.execute(query)
    return redirect(reverse("home"))


def add_as_sibling(request):
    if request.method == "POST":
        form = DocumentItemForm(request.POST)
        if form.is_valid():
            new_counterpoint = form.save()
            sibling = DocumentItem.objects.get(id=request.POST.get('parent'))
            new_counterpoint.parent = sibling.parent
            new_counterpoint.save()
            parent = DocumentItem.objects.get(id=sibling.parent)
            for x in DocumentItem.objects.filter(lft__gt=parent.rgt):
                x.lft = x.lft + 2
                x.save()
            for y in DocumentItem.objects.filter(rgt__gt=parent.rgt):
                y.rgt = y.rgt + 2
                y.save()
            return redirect('home')

        else:
            context = {'form', form}
            return render(request, '', context)
    else:
        context = {form: DocumentItemForm()}
        return render(request, '', context)
    

class SectionDeleteModelView(DeleteView):
    model = DocumentItem
    success_url = reverse_lazy('home')


def delete_document_item(request):
    pass


def bibliotheque_item_detail_view(request, pk):
    library_item_obj: DocumentItem = DocumentItem.objects.get(id=pk)
    context = {"library_item_obj": library_item_obj}
    return render(request, "bibliotheque/home.html", context)


def render_hierarchical_data(request, root_id=2):

    tree = DocumentItem.objects.get(id=root_id).get_tree
    context = {"tree": tree}
    return render(request, 'bibliotheque/hierarchy.html', context)


def counterpoint_add(request, pk=None):
    """
    This view adds a counterpoint to an allegation, either as a child of this allegation
    or as a sibling of another counterpoint. The discrimination is based on the desc of the itme.

    Args:
        request:
        pk: primary key to the the

    Returns:

    """

    if pk:
        relative = DocumentItem.objects.get(id=pk)
    else:
        relative = DocumentItem.objects.get(id=request.POST.get('parent_id'))

    if relative.desc.id == 1:  # relative is a parent
        parent = relative
        parameter = relative.lft

    elif relative.desc.id == 2:  # relative is a sibling
        parent = DocumentItem.objects.get(id=relative.parent)
        parameter = relative.rgt
    else:
        parameter = None
        parent = None

    if request.method == "POST":

        title_form = CounterPointModelForm(request.POST)
        # text_form = DocumentTextModelForm(request.POST)

        if title_form.is_valid() and parameter is not None:
            for item in DocumentItem.objects.filter(lft__gt=parameter):
                item.lft = item.lft + 2
                item.save()
            for item in DocumentItem.objects.filter(rgt__gt=parameter):
                item.rgt = item.rgt + 2
                item.save()
            title = title_form.save()
            return redirect('home')

        else:
            context = {'parent': parent,
                       'item_form': title_form
                       }
            return render(request, 'bibliotheque/counterpoint_item_text_form.html', context)

    else:

        item_form = CounterPointModelForm({'parent': parent.id,
                                                'lft': parameter + 1,
                                                'rgt': parameter + 2,
                                                'desc': TypeDocument.objects.get(id=2)})



        context = {'parent': parent,
                   'item_form': item_form
                   }
        return render(request, 'bibliotheque/counterpoint_item_text_form.html', context)


def allegation_add(request, pk=None):
    if pk is None:
        pk = request.POST.get("parent")

    sibling = DocumentItem.objects.get(id=pk)

    if request.method == "POST":
        request.POST._mutable = True
        form = RequeteItemModelForm(request.POST)
        form.data["desc"] = TypeDocument.objects.get(id=1)

        # form.save(commit=False)
        if form.is_valid():
            parameter = sibling.rgt
            for item in DocumentItem.objects.filter(rgt__gt=parameter):
                item.rgt = item.rgt + 2
                item.save()
            for item in DocumentItem.objects.filter(lft__gt=parameter):
                item.lft = item.lft + 2
                item.save()
            form.save()
            return redirect('home')
        else:

            context = {'form': form,
                       'sibling': sibling
                       }
            return render(request, 'bibliotheque/allegation_item_form.html', context)
    else:
        item_form = RequeteItemModelForm({'parent': sibling.id,
                                          'lft': sibling.rgt + 1,
                                          'rgt': sibling.rgt + 2,
                                          'is_true': True})
        context = {'form': item_form,
                   'sibling': sibling
                   }
        return render(request, 'bibliotheque/allegation_item_form.html', context)


@csrf_exempt
def ajax_return_item_object(request):
    document_item_obj = DocumentItem.objects.get(id=request.POST.get("sibling_id"))

    document_item_dict = {"id_parent": document_item_obj.id,
                          "id_lft": document_item_obj.rgt + 1,
                          "id_rgt": document_item_obj.rgt + 2,
                          "item": document_item_obj.item}

    data = JsonResponse(document_item_dict, safe=False)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def timelinejs_add(request):

    if request.method == 'POST':
        # pass
        # relative = DocumentItem.objects.get(id=request.post.get("relative_id"))
        relative = DocumentItem.objects.get(id=request.POST.get("timeline_related_item"))
        if relative.desc.id == 1:
        #     insert as child
            parameter = relative.lft
            parent_id = relative.id
        else:
        #     insert as sibbling
            parameter = relative.rgt
            parent_id = relative.parent

        rgt_parameter_to_be_update_qs = DocumentItem.objects.filter(rgt__gt=parameter)

        lft_parameter_to_be_update_qs = DocumentItem.objects.filter(lft__gt=parameter)

        form = DocumentItemForm({'parent': parent_id,
                                 'lft': parameter + 1,
                                 'rgt': parameter + 2,
                                 'desc': TypeDocument.objects.get(id=3),
                                 'item': request.POST.get("timeline_id"),
                                 'is_true': 1
                                 })
        if form.is_valid():
            form.save()

            for x in rgt_parameter_to_be_update_qs:
                x.rgt = x.rgt + 2
                x.save()

            for y in lft_parameter_to_be_update_qs:
                y.lft = y.lft + 2
                y.save()

            return redirect('home')
        else:
            context = {}
            return render(request, 'bibliotheque/home.html', context)
    else:
        context={}
        return render(request, 'bibliotheque/home.html', context)


def requete(request):
    doc = DocumentItem.objects.get(id=2)
    root = doc.get_tree_old
    previous_depth=0
    i = 1
    for dict_ in root:
        if dict_["depth"] !=0:
            dict_["requete_number"] = i
            i += 1

        this_depth = dict_["depth"]
        dict_["previous_depth"] = previous_depth

        if previous_depth - this_depth   > 0:
            dict_["range"] = range(previous_depth - this_depth)
        else:
            dict_["range"] = ""

        previous_depth = this_depth

    context = {'document': root,
               'item': doc}
    return render(request, 'bibliotheque/requete.html', context)


def rebuttal(request, pk):
    allegation = DocumentItem.objects.get(id=pk)
    context={'allegation': allegation}
    return render(request, 'bibliotheque/rebuttal.html', context)

def get_image_list_old(request):
    images = Flickr.objects.all()
    image_list = [{'title': img.title, 'value': img.link_to_original_photo} for img in images]
    return JsonResponse(image_list, safe=False)

def get_image_list(request):
    images = FlikrPhoto.objects.all()
    # thumbnails = FlikrPhoto.objects.filter(label="Thumbnail")
    # original = FlikrPhoto.objects.filter(label="Original")
    image_list = [{'title': img.headline, 
                   "text": img.text, 
                   'value': img.source} for img in images if img.label == "Original"]
    # image_list = [{'title': thumb.headline, 
    #                "text": thumb.text, 
    #                'value': f'<a href="{orig.source}" target="_blank"><img src="{thumb.source}" alt="{thumb.headline}" /></a>'
    #                } for thumb, orig in zip(thumbnails, original)
    #                ]
    # `<a href="${item.o_link}" target="_blank"><img src="${item.value}" alt="${item.title}" /></a>`
    return JsonResponse(image_list, safe=False)