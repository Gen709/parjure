from django.forms import ModelForm
from .models import DocumentItem, TypeDocument
from django import forms


class DocumentItemForm(ModelForm):

    class Meta:
        model = DocumentItem
        fields = "__all__"

    # def save_as_child(self, commit=True):
    #
    #     instance = super(DocumentItemForm, self).save(commit=False)
    #
    #     lft_itme_qs = DocumentItem.objects.filter(lft__gt=instance.parent_id)
    #     rgt_item_qs = DocumentItem.objects.filter(rgt__gt=instance.parent_id)
    #
    #     for item_lft, item_rgt in zip(lft_itme_qs, rgt_item_qs):
    #         item_lft.lft = item_lft.lft + 2
    #         item_rgt.rgt = item_rgt.rgt + 2
    #         item_lft.save()
    #         item_rgt.rgt.save()
    #
    #     if commit:
    #         instance.save()
    #
    #     return instance
    #
    # def save_as_sibling(self, commit=True):
    #     instance = super(DocumentItemForm, self).save(commit=False)
    #
    #     if commit:
    #         instance.save()
    #
    #     return instance


class RequeteItemModelForm(DocumentItemForm):
    # desc = forms.ModelChoiceField(queryset=TypeDocument.objects.get(id=1),
    #                               widget=forms.HiddenInput())
    class Meta:
        model = DocumentItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget = forms.HiddenInput()
        self.fields['lft'].widget = forms.HiddenInput()
        self.fields['rgt'].widget = forms.HiddenInput()
        self.fields['desc'].widget = forms.HiddenInput(attrs={'value': TypeDocument.objects.get(id=1)})
        self.fields['item'].widget = forms.Textarea(attrs={'rows': 4})
        self.fields['text'].widget = forms.HiddenInput(attrs={'value': None})
        self.fields['is_true'].widget = forms.HiddenInput(attrs={'value': False})


class CounterPointModelForm(DocumentItemForm):
    class Meta:
        model = DocumentItem
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].widget = forms.HiddenInput()
        self.fields['lft'].widget = forms.HiddenInput()
        self.fields['rgt'].widget = forms.HiddenInput()
        self.fields['desc'].widget = forms.HiddenInput(attrs={'value': TypeDocument.objects.get(id=2)})
        self.fields['item'].widget = forms.Textarea(attrs={'rows': 1, 'placeholder': 'Titre de la section'})
        self.fields['item'].label = "Titre de la section"
        self.fields['text'].widget = forms.Textarea(attrs={'rows': 6, 'placeholder': 'Détails'})
        self.fields['item'].label = "Détails de la section"
        self.fields['is_true'].widget = forms.HiddenInput(attrs={'value': None})

