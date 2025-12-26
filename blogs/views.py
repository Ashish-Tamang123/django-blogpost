from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Blog, Category

def post_by_category(request, category_id):
    # Fetch the post that belongs to the category with id category_id
    posts = Blog.objects.filter(status='Published', category=category_id)

    # Use try/except when we want to do some custom action if the category does not exist
    try:
        category = Category.objects.get(pk=category_id)
    except:
        # redirect the user to homepage
        return redirect('home')
    
    # Use get_object_or_404 when you want to show error page if the category does not exist
    # category = get_object_or_404(Category, pk=category_id)
    context = {
        'posts': posts,
        'category': category, 
    }
    return render(request, 'post_by_category.html', context)
