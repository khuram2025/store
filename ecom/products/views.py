from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ProductImage
from .forms import CategoryForm, ProductForm, CategorySelectForm, ProductImageFormSet 

def select_category(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        form = CategorySelectForm(request.POST)
        if form.is_valid():
            request.session['selected_category_id'] = form.cleaned_data['category'].id

            return redirect('products:add_product_form')
        else:
            print(form.errors)  # Log the form errors
    else:
        form = CategorySelectForm()

    return render(request, 'products/select_category.html', {'form': form, 'categories': categories})

def add_product_form(request):
    selected_category_id = request.session.get('selected_category_id')
    if not selected_category_id:
        return redirect('select_category')
    category = Category.objects.get(id=selected_category_id)
    if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, category=category) # Add request.FILES
            if form.is_valid():
                product_instance = form.save()

                # Handle image uploads
                uploaded_images = request.FILES.getlist('product_images')
                for image_file in uploaded_images:
                    ProductImage.objects.create(product=product_instance, image=image_file)                
                return redirect('product_list')
            else:
                image_formset = ProductImageFormSet(request.POST, request.FILES)
    else:
        form = ProductForm(category=category)
        image_formset = ProductImageFormSet(queryset=ProductImage.objects.none())

    fields_to_exclude = ['title', 'description', 'regular_price', 'discount_price', 'youtube_link', 'facebook_link', 'web_link']

    return render(request, 'products/add_product_form.html', {'form': form, 'fields_to_exclude': fields_to_exclude, 'image_formset': image_formset})


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

    return render(request, 'pwa/products/products_by_category.html', {'products': products, 'category': category, 'subcategories': subcategories})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    images = product.product_image.all()
    featured_image = None
    other_images = []
    for image in images:
        if image.is_feature:
            featured_image = image
        else:
            other_images.append(image)
    discount_percentage = 0
    if product.regular_price > 0 and product.discount_price:
        discount_percentage = (product.regular_price - product.discount_price) / product.regular_price * 100
    return render(request, 'pwa/products/product_detail.html', {'product': product, 'featured_image': featured_image, 'other_images': other_images, 'discount_percentage': discount_percentage})
