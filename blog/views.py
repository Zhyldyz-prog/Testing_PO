
from django.shortcuts import render, get_object_or_404
from .models import Blog


def blog_list_view(request):
    blogs = Blog.objects.all().order_by('-id')

    return render(
        request,
        'blog/blog_list.html',
        {'blogs': blogs}
    )


def blog_detail_view(request, id):
    blog = get_object_or_404(Blog, id=id)

    blog.views += 1
    blog.save(update_fields=['views'])

    return render(
        request,
        'blog/blog_detail.html',
        {'blog': blog}
    )
