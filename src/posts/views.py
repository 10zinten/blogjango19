from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .forms import PostForm
from .models import Post

def post_create(request):
	form = PostForm(request.POST)
	if form.is_valid():
		instance = form.save(commit=False)
		print form.cleaned_data.get("title")
		instance.save()

	# if request.method == "POST":
	# 	print request.POST.get("title")
	# 	print request.POST.get("content")
	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

def post_detail(request, id=None): #retrieve
	instance = get_b=get_object_or_404(Post, id=id)
	context = {
		"title": instance.title,
		"instance": instance
	}
	return render(request, "post_detail.html", context)

def post_list(request): #list items
	queryset = Post.objects.all()
	context = {
		"object_lists": queryset,
		"title": "List"
	 }

	# if request.user.is_authenticated():
	# 	context = {
	# 		"title": "My user List"
	# 	}
	# else:
	# 	context = {
	# 		"title": "List"
	# 	}
	return render(request, "index.html", context)
	#return HttpResponse("<h1>List</h1>")

def post_update(request):
	return HttpResponse("<h1>Update</h1>")

def post_delete(request):
	return HttpResponse("<h1>Delete</h1>")