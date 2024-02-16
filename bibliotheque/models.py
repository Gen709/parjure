from django.db import models, connection
from django.urls import reverse
import re
# from .forms import DocumentItemForm

# http://mikehillyer.com/articles/managing-hierarchical-data-in-mysql/
# https://stackoverflow.com/questions/805393/what-is-the-best-way-to-access-stored-procedures-in-djangos-orm
# Create your models here.


def clean_text(item):
    cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    if item != "" and (type(item) == str):
        cleantext = re.sub(cleanr, '', item)
        return cleantext


class TypeDocument(models.Model):
    desc = models.CharField(max_length=100)

    def __str__(self):
        return self.desc

class DocumentItem(models.Model):
    """
    is_leaf

    get_parent

    get_item_free_of_html

    get_tree

    get_related

    text
    """
    parent = models.IntegerField(null=True)
    lft = models.IntegerField()
    rgt = models.IntegerField()
    item = models.TextField()
    text = models.TextField(null=True, blank=True)
    desc = models.ForeignKey(TypeDocument, on_delete=models.SET_NULL, null=True)
    is_true = models.BooleanField(null=True, default=True)
    # depth = models.SmallIntegerField(null=True, default=None)


    @property
    def width(self):
        return int(self.rgt) - int(self.lft) + 1

    @property
    def get_children(self):
        if self.width == 2:
            return None
        else:
            return DocumentItem.objects.filter(lft__gt=self.lft).filter(lft__lt=self.rgt).order_by('lft')

    @property
    def get_parent(self):
        return self.get_path[-1]

    @property
    def get_item_free_of_html(self):
        cleanr = re.compile('<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
        if self.item != "" and (type(self.item) == str):
            cleantext = re.sub(cleanr, '', self.item)
            return cleantext

    @property
    def get_tree_old(self):
        element_dict_list = []
        with connection.cursor() as cursor:
            cursor.execute("CALL get_tree_with_depth_raw(" + str(self.id) + ",1)")
            data = cursor.fetchall()

            for row in data:
                data_dict = {"depth": row[6], "document_item_obj": DocumentItem.objects.get(id=row[0])}
                element_dict_list.append(data_dict)

            i = 1
            previous_depth = 0
            for data_dict in element_dict_list:
                if data_dict["depth"] != 0:
                    data_dict["requete_number"] = i
                    i += 1
                this_depth = data_dict["depth"]
                data_dict["previous_depth"] = previous_depth

                if previous_depth - this_depth > 0:
                    data_dict["range"] = range(previous_depth - this_depth)
                else:
                    data_dict["range"] = ""
                previous_depth = this_depth

        return element_dict_list

    @property
    def get_tree(self):
        element_dict_list = []
        with connection.cursor() as cursor:
            cursor.execute("CALL get_tree_with_depth(" + str(self.id) + ")")
            data = cursor.fetchall()

            for row in data:
                data_dict = {"depth": row[3], "document_item_obj": DocumentItem.objects.get(id=row[0])}
                element_dict_list.append(data_dict)

            
            previous_depth = 0
            for data_dict in element_dict_list:

                this_depth = data_dict["depth"]
                data_dict["previous_depth"] = previous_depth
                
                if previous_depth - this_depth == 1:
                    data_dict["range"] = range(1)
                elif previous_depth - this_depth > 1:
                    data_dict["range"] = range(previous_depth - this_depth - 1) 
                else:
                    data_dict["range"] = ""
                previous_depth = this_depth

        return element_dict_list


    @property
    def get_related(self):
        element_dict_list = []
        with connection.cursor() as cursor:
            cursor.execute("CALL get_tree_with_depth_raw(" + str(self.id) + ",3)")
            data = cursor.fetchall()
            for row in data:
                data_dict = {"depth": row[6],
                             "document_item_obj": DocumentItem.objects.get(id=row[0])
                             }
                element_dict_list.append(data_dict)

            i = 1
            previous_depth = 0
            for data_dict in element_dict_list:
                if data_dict["depth"] != 0:
                    data_dict["requete_number"] = i
                    i += 1
                this_depth = data_dict["depth"]
                data_dict["previous_depth"] = previous_depth

                if previous_depth - this_depth > 0:
                    data_dict["range"] = range(previous_depth - this_depth)
                else:
                    data_dict["range"] = ""
                previous_depth = this_depth

        return element_dict_list

    @property
    def get_path(self):
        element_obj_list = []
        with connection.cursor() as cursor:
            cursor.execute("CALL get_single_path(" + str(self.id) + ")")
            data = cursor.fetchall()
            for row in data:
                d = DocumentItem.objects.get(id=row[0])
                element_obj_list.append(d)
        return element_obj_list[1:]

    def assign_as_a_children_to(self, parent_id):
        if self.is_leaf:
            element_obj_list = []
            with connection.cursor() as cursor:
                # add the children
                cursor.execute("CALL add_child_nod(" + str(parent_id) + str(self.item) + ")")
                self.delete()
                cursor.execute("CALL get_tree_with_depth_raw(" + str(parent_id) + ")")
                data = cursor.fetchall()
                for row in data:
                    d = DocumentItem.objects.get(id=row[0])
                    element_obj_list.append(d)
            return element_obj_list
        else:
            return "Element has children, deal with the children first"

    def assign_as_sibling_to(self, sibling_id):
        if self.is_leaf:
            element_obj_list = []
            with connection.cursor() as cursor:
                # add the children
                cursor.execute("CALL add_sibling_nod(" + str(sibling_id) + ", '" + self.item + "')")
                parent_id = self.parent
                self.delete()

                cursor.execute("CALL get_tree_with_depth_raw(" + str(parent_id) + ")")
                data = cursor.fetchall()
                for row in data:
                    d = DocumentItem.objects.get(id=row[0])
                    element_obj_list.append(d)
            return element_obj_list
        else:
            return "Element has children, deal with the children first"

    def __str__(self):
        return str(self.id) + " " + self.get_item_free_of_html

   



class DocumentText(models.Model):
    document_section = models.OneToOneField(DocumentItem, on_delete=models.CASCADE, primary_key=True)
    text = models.TextField()
