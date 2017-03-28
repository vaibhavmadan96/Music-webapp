from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Album,Song
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.views.generic import View
from .forms import UserForm, AlbumForm
from django.http import JsonResponse

# class IndexView(generic.ListView):
# 	template_name= 'music/index.html'

# 	def get(self,request):
# 		if not request.user.is_authenticated():
# 			return render(request, 'music/login.html')
# 		else:
# 		    return Album.objects.filter(user=request.user)
# 		#return Album.objects.all()

IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        albums = Album.objects.filter(user=request.user)
       	return render(request, 'music/index.html', {'albums': albums})

def detail(request, album_id):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'music/detail.html', {'album': album, 'user': user})

		
def create_album(request):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            file_type = album.album_logo.url.split('.')[-1]#-1 object in list created by split(',')
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'music/album_form.html', context)
            album.save()
            return render(request, 'music/detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'music/album_form.html', context)
		
# class AlbumUpdate(UpdateView):
# 	model=Album
# 	fields=['artist','album_title','genre','album_logo']

def favorite_album(request,album_id):
	album=get_object_or_404(Album,pk=album_id)
	try:
		if album.is_favorite:
			album.is_favorite=False
		else:
			album.is_favorite=True
		album.save()
	except (KeyError, Album.DoesNotExist):
		return JsonResponse({'success':False})
	else:
		return JsonResponse({'success':True})


def delete_album(request,album_id):
	album=Album.objects.get(pk=album_id)
	album.delete()
	albums=Album.objects.filter(user=request.user)
	return render(request,'music/index.html',{'albums':albums})

def logout_user(request):
    logout(request)
    form=UserForm(None)
    return render(request,'music/login.html',{'form':form})	

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return render(request, 'music/index.html', {'albums': albums})
            else:
                return render(request, 'music/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'music/login.html', {'error_message': 'Invalid login'})
    return render(request, 'music/login.html')


class UserFormView(View):
	form_class = UserForm
	template_name='music/registration_form.html'

	#display balnk form
	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})

	# process form data
	def post(self,request):
		form=self.form_class(request.POST or None)

		if form.is_valid():
			user=form.save(commit=False)

			#cleaned (normalised) data
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user.set_password(password)
			user.save()

			#return user object if credentials are correct
			user=authenticate(username=username,password=password)

			if user is not None:
				if user.is_active:
					login(request,user)#loggedin request.user.username
					return redirect('music:index')

		return render(request,self.template_name,{'form':form})


def songs(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'music/login.html')
    else:
        try:
            song_ids = []
            for album in Album.objects.filter(user=request.user):
                for song in album.song_set.all():
                    song_ids.append(song.pk)
            users_songs = Song.objects.filter(pk__in=song_ids)
            if filter_by == 'favorites':
                users_songs = users_songs.filter(is_favorite=True)
        except Album.DoesNotExist:
            users_songs = []
        return render(request, 'music/songs.html', {
            'song_list': users_songs,
            'filter_by': filter_by,
        })


