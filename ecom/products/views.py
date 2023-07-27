from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from .forms import CategoryForm, ProductForm


def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, 'backend/admin_category.html', {'categories': categories})

def category_list(request):
    parent_categories = Category.objects.filter(parent__isnull=True)
    return render(request, 'pwa/products/category_wide.html', {'categories': parent_categories})


def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    return render(request, 'categories/category_detail.html', {'category': category})

def category_new(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save()
            return redirect('products:admin_category_list', slug=category.slug)
        else:
            print(form.errors)  # Add this line to print form errors
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


def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'backend/admin_products.html', {'products': products})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_edit.html', {'form': form})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def products_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    subcategories = Category.objects.filter(parent=category)
    products = Product.objects.filter(category__in=[category] + list(subcategories))

    return render(request, 'pwa/products/products_by_category.html', {'products': products})
