from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('mahsulotlar/', views.product_list, name='product_list'),
    path('mahsulot/<slug:slug>/', views.product_detail, name='product_detail'),
    path('savat/', views.cart_view, name='cart'),
    path('savat/qoshish/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('savat/yangilash/<int:item_id>/', views.update_cart, name='update_cart'),
    path('buyurtma/', views.checkout, name='checkout'),
    path('buyurtma/muvaffaqiyat/<int:order_id>/', views.order_success, name='order_success'),
    path('buyurtmalarim/', views.order_list, name='order_list'),
    path('buyurtma/<int:order_id>/', views.order_detail, name='order_detail'),
    path('royxat/', views.register_view, name='register'),
    path('kirish/', views.login_view, name='login'),
    path('chiqish/', views.logout_view, name='logout'),
    path('profil/', views.profile, name='profile'),
]
