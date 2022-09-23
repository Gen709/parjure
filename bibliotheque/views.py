from django.shortcuts import render, redirect
from .models import Library

from django.db import connection


def home(request):
    context = {}
    return render(request, "bibliotheque/home.html", context)


def get_full_tree(request):
    parent_id = request.GET.get("parent_id", 1)

    with connection.cursor() as cursor:
        cursor.execute("CALL get_tree_with_depth(" + str(parent_id) + ")")
        data = cursor.fetchall()

    context = {"tree": data}
    return render(request, "bibliotheque/home.html", context)


def bibliotheque_text_update(request):
    library_item_obj: Library = Library.objects.get(id=request.POST.get('requete_section_id'))
    library_item_obj.item=request.POST.get('requete_item_text')
    library_item_obj.save()
    return redirect('home')
