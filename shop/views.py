from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q, Avg
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Review


def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key, user=None)
    return cart


def home(request):
    featured_products = Product.objects.filter(is_featured=True, is_available=True)[:8]
    new_products = Product.objects.filter(is_available=True).order_by('-created_at')[:8]
    categories = Category.objects.all()[:6]
    sale_products = Product.objects.filter(discount_price__isnull=False, is_available=True)[:4]
    return render(request, 'shop/home.html', {
        'featured_products': featured_products,
        'new_products': new_products,
        'categories': categories,
        'sale_products': sale_products,
    })


def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search_q = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '-created_at')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    material = request.GET.get('material')
    current_category = None

    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)
    if search_q:
        products = products.filter(Q(name__icontains=search_q) | Q(description__icontains=search_q))
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if material:
        products = products.filter(material=material)

    valid_sorts = ['-created_at', 'price', '-price', 'name', '-name']
    if sort_by in valid_sorts:
        products = products.order_by(sort_by)

    return render(request, 'shop/product_list.html', {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'search_q': search_q,
        'sort_by': sort_by,
        'material_choices': [
            ('yogoch', "Yog'och"), ('metal', 'Metal'), ('plastik', 'Plastik'),
            ('shisha', 'Shisha'), ('mato', 'Mato'), ('teri', 'Teri'), ('aralash', 'Aralash'),
        ],
        'selected_material': material,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        if rating and comment:
            Review.objects.update_or_create(
                product=product, user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            messages.success(request, "Sharhingiz qo'shildi!")
            return redirect('product_detail', slug=slug)

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'user_review': user_review,
        'star_range': range(1, 6),
    })


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_available=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += quantity
    else:
        item.quantity = quantity
    item.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.total_items, 'message': f"{product.name} savatga qo'shildi!"})
    messages.success(request, f"{product.name} savatga qo'shildi!")
    return redirect('cart')


def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'shop/cart.html', {'cart': cart})


@require_POST
def update_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    action = request.POST.get('action')
    if action == 'increase':
        item.quantity += 1
        item.save()
    elif action == 'decrease':
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
        else:
            item.delete()
    elif action == 'remove':
        item.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': cart.total_items, 'cart_total': str(cart.total_price)})
    return redirect('cart')


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Savatingiz bo'sh!")
        return redirect('cart')
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        city = request.POST.get('city')
        notes = request.POST.get('notes', '')
        if full_name and phone and address and city:
            order = Order.objects.create(
                user=request.user, full_name=full_name, phone=phone,
                address=address, city=city, notes=notes, total_price=cart.total_price,
            )
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order, product=item.product, product_name=item.product.name,
                    price=item.product.final_price, quantity=item.quantity,
                )
            cart.items.all().delete()
            messages.success(request, f"Buyurtma #{order.id} muvaffaqiyatli joylashtirildi!")
            return redirect('order_success', order_id=order.id)
        else:
            messages.error(request, "Iltimos, barcha maydonlarni to'ldiring.")
    return render(request, 'shop/checkout.html', {'cart': cart})


@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_success.html', {'order': order})


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'shop/order_list.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'shop/order_detail.html', {'order': order})


def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Ro'yxatdan o'tish muvaffaqiyatli!")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'shop/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'shop/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user)[:5]
    return render(request, 'shop/profile.html', {'orders': orders})
