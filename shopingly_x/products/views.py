from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Category, Product
from cart.forms import CartAddProductForm


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(is_active=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    sort = request.GET.get('sort')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'rating':
        products = products.order_by('-rating')

    paginator = Paginator(products, 12)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
        'products': page_obj.object_list,
    })


def product_search(request):
    query = request.GET.get('q', '').strip()
    products = Product.objects.filter(is_active=True)
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': Category.objects.all(),
        'query': query,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, is_active=True)
    cart_product_form = CartAddProductForm()
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(id=product.id)[:4]
    return render(request, 'products/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'related_products': related_products,
    })
