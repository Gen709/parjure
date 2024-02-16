from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from .models import Flickr, Album
from .forms import FlickrModelForm, FlickrAlbumModelForm, FlickrAlbumNoPhotosModelForm

# Create your views here.


class FlickrPhotoDetailView(DetailView):
    model = Flickr
    context_object_name = "photo"
    queryset = Flickr.objects.all()
    # template_name = 'flickr/photo_detail.html'


class FlickrPhotoUpdateView(UpdateView):
    model = Flickr
    context_object_name = "photo"
    # template_name = 'flickr/flickr_form.html'
    fields = '__all__'


def flickr_update_view(request, pk):
    f = Flickr.objects.get(id=pk)
    if request.method == "POST":
        form = FlickrModelForm(request.POST, instance=f)
        if form.is_valid():
            form.save()
            return redirect('flicker-list-view')
    else:
        form = FlickrModelForm(instance=f)

    return render(request, 'flickr/flickr_form.html', {'form': form, 'pk': pk, 'photo': f})


class FlickrPhotoDeleteView(DeleteView):
    model = Flickr
    success_url = reverse_lazy('flicker-list-view')


class FlickrPhotosListView(ListView):
    queryset = Flickr.objects.order_by('date_taken_obj')
    context_object_name = "photo_list"
    template_name = 'flickr/photo_list.html'


class FlickrAlbumPhotosListView(ListView):
    template_name = 'flickr/photo_by_album.html'

    def get_queryset(self):
        return Flickr.objects.filter(album__id=self.kwargs['album_id'])


def album_create(request):
    if request.method == "POST":
        # request.POST._mutable = True
        form = FlickrAlbumModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('album-list-view')
        else:
            selected_photos = request.POST.get("photos")
            photos = Flickr.objects.all().order_by('date_taken_obj')
            form = FlickrAlbumNoPhotosModelForm(request.POST)
            context={'selected_photos': selected_photos,
                     'photos': photos,
                     'form': form
                     }
            return render(request, 'flickr/album_create_form.html', context)
    else:
        photos = Flickr.objects.all().order_by('date_taken_obj')
        form = FlickrAlbumNoPhotosModelForm()
        context={'form': form, 'photos': photos}
        return render(request, 'flickr/album_create_form.html', context)


class AlbumCreateView(CreateView):
    model = Album
    form_class = FlickrAlbumModelForm
    success_url = 'album-list-view'


class AlbumDetailView(DetailView):
    model = Album
    template_name_suffix = '_details'


class AlbumListView(ListView):
    model = Album
    context_object_name = 'album_list'


class AlbumUpdateView(UpdateView):
    model = Album
    fields = '__all__'
    template_name_suffix = '_update_form'
    success_url = 'album-list-view'


class AlbumDeleteView(DeleteView):
    model = Album
    success_url = reverse_lazy('album-list-view')

def json_flickr_data(request):
    context={}
    return redirect(request, "", context)