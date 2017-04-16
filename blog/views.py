from django.shortcuts import render
from blog.models import Post
from django.utils import timezone

def post_list(request, header):
    print(header)
    print(request)
    print(type(header))
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

