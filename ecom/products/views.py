from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, ProductImage, ProductSpecificationValue
from .forms import CategoryForm, ProductForm, CategorySelectForm, ProductImageFormSet 
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone



def select_category(request):
    # Fetch only parent categories (categories without a parent)
    parent_categories = Category.objects.filter(parent__isnull=True)

    if request.method == 'POST':
        form = CategorySelectForm(request.POST)
        if form.is_valid():
            request.session['selected_category_id'] = form.cleaned_data['category'].id
            return redirect('products:add_product_form')
        else:
            print(form.errors)  # Log the form errors
    else:
        form = CategorySelectForm()

    return render(request, 'products/select_category.html', {'form': form, 'categories': parent_categories})


def add_product_form(request):
    selected_category_id = request.session.get('selected_category_id')
    if not selected_category_id:
        return redirect('select_category')
    
    category = Category.objects.get(id=selected_category_id)
    
    initial_data = {}
    if request.user.is_authenticated:
        initial_data = {
            'seller_name': request.user.name,
            'seller_mobile': request.user.mobile_number,
            'seller_city': request.user.userprofile.city
        }
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, category=category, user=request.user)

        if form.is_valid():
            product_instance = form.save(commit=False)
            product_instance.seller_name = request.POST.get('seller_name')
            product_instance.seller_mobile = request.POST.get('seller_mobile')
            product_instance.seller_city = request.POST.get('seller_city')
            product_instance = form.save()

            # Handle image uploads
            uploaded_images = request.FILES.getlist('product_images')
            for image_file in uploaded_images:
                ProductImage.objects.create(product=product_instance, image=image_file)

            return redirect('product_list')
        image_formset = ProductImageFormSet(request.POST, request.FILES)
    else:
        form = ProductForm(category=category, user=request.user, initial=initial_data) # Pass the initial data here
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
    main_category = get_object_or_404(Category, slug=slug, parent__isnull=True, is_active=True)

    # Fetch the direct children (subcategories) of this main category
    subcategories = main_category.get_children()

    # Dictionary to hold products for each subcategory
    products_by_subcategory = {}
    for subcategory in subcategories:
        products_by_subcategory[subcategory] = Product.objects.filter(category=subcategory, is_active=True)
  

    context = {
        'main_category': main_category,
        'subcategories': subcategories,
        'products_by_subcategory': products_by_subcategory,
    }
    
    return render(request, 'suha/category.html', context)

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
    
    # Fetching product specifications
    product_specifications = ProductSpecificationValue.objects.filter(product=product)
    now = timezone.now()

    if product.updated_at > product.created_at:
        # If the product was updated after it was created, use the updated_at date
        delta = relativedelta(now, product.updated_at)
        action = "Updated"
    else:
        delta = relativedelta(now, product.created_at)
        action = "Posted"

    months = delta.months
    days = delta.days

    return render(request, 'suha/product_detail.html', {
        'product': product,
        'featured_image': featured_image,
        'other_images': other_images,
        'discount_percentage': discount_percentage,
        'product_specifications': product_specifications,  # Passing the specifications to the template
        'months': months,
        'days': days,
        'action':action
    })
