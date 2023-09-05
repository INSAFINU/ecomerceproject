from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.core.paginator import Paginator,EmptyPage,InvalidPage

def allProdCat(request, c_slug=None):
    category = None
    products_list = Product.objects.filter(available=True)

    if c_slug:
        category = get_object_or_404(Category, slug=c_slug)
        products = products_list.filter(category=category)
    else:
        paginator = Paginator(products_list, 6)
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            page = 1
        try:
            products = paginator.page(page)
        except (EmptyPage, InvalidPage):
            products = paginator.page(paginator.num_pages)

    return render(request, 'category.html', {'category': category, 'products': products})



# def proDetail(request, c_slug, product_slug):
#     Product = get_object_or_404(Product, category__slug=c_slug, slug=product_slug)
#
#     return render(request, 'Product.html', {'Product': Product})
def product_detail(request, c_slug, product_slug):
    product = get_object_or_404(Product, category__slug=c_slug, slug=product_slug)
    return render(request, 'product.html', {'product': product})
def home_page(request):
    return render(request,'mn.html')