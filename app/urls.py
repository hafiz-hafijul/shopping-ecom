from django.urls import path
from app import views


urlpatterns = [
    path('', views.ProductView.as_view(), name='productshow'),
    path('product-detail/<int:pk>/',
         views.ProductDetailView.as_view(), name='product-detail'),

    path('add-to-cart/', views.add_to_cart, name='addcart'),
    path('cart/', views.show_cart, name='cart'),
    path('pluscart/', views.plus_cart),
    path('minuscart/', views.minus_cart),
    path('removecart/', views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('address/', views.address, name='address'),

    path('mobile/', views.mobile, name='mobile'),
    path('mobiledata/<slug:data>/', views.mobile, name='mobiledata'),
    path('laptop/', views.laptop, name='laptop'),
    path('laptopdata/<slug:data>/', views.laptop, name='laptopdata'),
    path('topwear/', views.topwearfashion, name='topwear'),
    path('topweardata/<slug:data>/', views.topwearfashion, name='topweardata'),
    path('bottomwear/', views.bottomwearfashion, name='bottomwear'),
    path('bottomweardata/<slug:data>/',
         views.bottomwearfashion, name='bottomweardata'),

    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='payment'),
    path('orders/', views.orders, name='orders'),

    path('searchbar/', views.searchbar, name='searchbar'),

    # auth
    path('registration/', views.CustomerRegistrationView.as_view(),
         name='customerregistration'),
    path('accounts/login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('passwordchange/', views.MyPasswordChangeView.as_view(),
         name='passwordchange'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]
