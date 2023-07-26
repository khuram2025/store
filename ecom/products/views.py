from django.shortcuts import render, get_object_or_404, redirect
from .models import Category
from .forms import CategoryForm

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'backend/admin_category.html', {'categories': categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'categories/category_detail.html', {'category': category})

def category_new(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect('products:category_list', slug=category.slug)
    else:
        form = CategoryForm()
    return render(request, 'backend/admin_create_category.html', {'form': form, 'categories': categories})


def category_edit(request, slug):
    category = get_object_or_404(Category, slug=slug)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            return redirect('category_detail', slug=category.slug)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_edit.html', {'form': form})

def category_delete(request, slug):
    category = get_object_or_404(Category, slug=slug)
    category.delete()
    return redirect('category_list')