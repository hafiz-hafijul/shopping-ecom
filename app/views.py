from django.shortcuts import render, HttpResponseRedirect, redirect
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.http import JsonResponse
from .models import Product, Cart, OrderPlaced, Customer
from .forms import CustomerRegistrationForm, LoginForm, MyPasswordChangeForm, CustomerProfileForm


class ProductView(View):
    def get(self, request):
        totalitem = 0
        topwear = Product.objects.filter(category='TW')
        bottomwears = Product.objects.filter(category='BM')
        laptop = Product.objects.filter(category='L')
        mobiles = Product.objects.filter(category='M')
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/home.html',
                      {'topwear': topwear, 'bottomwears': bottomwears, 'laptop': laptop, 'mobiles': mobiles, 'totalitem':totalitem})


class ProductDetailView(DetailView):
    def get(self, request, pk):
        totalitem = 0
        product = Product.objects.get(pk=pk)
        item_already_in_cart = False
        if request.user.is_authenticated:
            item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html', {'product': product, 'item_already_in_cart': item_already_in_cart, 'totalitem': totalitem})

@login_required
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product_ins = Product.objects.get(id=product_id)
    cus = Cart(user=user, product=product_ins, quantity=1)
    cus.save()
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return redirect('/cart')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        total_amount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                total_amount = amount + shipping_amount
                if request.user.is_authenticated:
                    totalitem = len(Cart.objects.filter(user=request.user))
            return render(request, 'app/addtocart.html', {'carts': cart, 'amount': amount, 'totalamount': total_amount, 'totalitem': totalitem})
        else:
            return render(request, 'app/emptycart.html')


@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)


@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

            data = {
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

            data = {
                'amount': amount,
                'totalamount': amount + shipping_amount
            }
            return JsonResponse(data)


def buy_now(request):
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/buynow.html', {'totalitem': totalitem})


@login_required
def address(request):
    add = Customer.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/address.html', {'add': add, 'active': 'btn-primary', 'totalitem': totalitem})



def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'xiaomi' or data == 'samsung' or data == 'oneplus':
        mobiles = Product.objects.filter(category='M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__lt=25000)
    elif data == 'above':
        mobiles = Product.objects.filter(
            category='M').filter(discounted_price__gt=25000)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/mobile.html', {'mobiles': mobiles, 'totalitem': totalitem})


def laptop(request, data=None):
    if data == None:
        Laptops = Product.objects.filter(category='L')
    elif data == 'Accer' or data == 'Lenevo' or data == 'hp':
        Laptops = Product.objects.filter(category='L').filter(brand=data)
    elif data == 'below':
        Laptops = Product.objects.filter(
            category='L').filter(discounted_price__lt=50000)
    elif data == 'above':
        Laptops = Product.objects.filter(
            category='L').filter(discounted_price__gt=50000)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/laptop.html', {'Laptops': Laptops, 'totalitem': totalitem})


def topwearfashion(request, data=None):
    if data == None:
        topwears = Product.objects.filter(category='TW')
    elif data == 'Polo' or data == 'Fu-Wang':
        topwears = Product.objects.filter(category='TW').filter(brand=data)
    elif data == 'below':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__lt=450)
    elif data == 'above':
        topwears = Product.objects.filter(category='TW').filter(discounted_price__gt=450)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/topwear.html', {'topwear': topwears, 'totalitem': totalitem})


def bottomwearfashion(request, data=None):
    if data == None:
        bottomwears = Product.objects.filter(category='BM')
    elif data == 'Zara' or data == 'Lee' or data == 'Denim':
        bottomwears = Product.objects.filter(category='BM').filter(brand=data)
    elif data == 'below':
        bottomwears = Product.objects.filter(
            category='BM').filter(discounted_price__lt=800)
    elif data == 'above':
        bottomwears = Product.objects.filter(
            category='BM').filter(discounted_price__gt=800)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/bottomwear.html', {'bottomwear': bottomwears, 'totalitem': totalitem})


@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)

    amount = 0.0
    shipping_amount = 70.0
    cart_products = [p for p in Cart.objects.all() if p.user == user]
    if cart_products:
        for p in cart_products:
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        total_amount = amount + shipping_amount
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/checkout.html', {'add': add, 'cart_items': cart_items, 'totalamount': total_amount, 'totalitem': totalitem})


@login_required
def payment_done(request):
    if request.method == 'GET':
        user= request.user
        pdid = request.GET.get('cusid')
        print(pdid)
        customer = Customer.objects.get(id=pdid)
        carts = Cart.objects.filter(user=user)
        for c in carts:
            op = OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity)
            op.save()
            c.delete()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return redirect('orders')


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request, 'app/orders.html', {'op': op, 'totalitem': totalitem})
    

def searchbar(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        post = Product.objects.all().filter(title=search)
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/search.html', {'post': post, 'totalitem': totalitem})


# Start Authentication All View


class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'app/customerregistration.html', {'form': form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
        return render(request, 'app/customerregistration.html', {'form': form})


class UserLoginView(LoginView):
    template_name = 'app/login.html'
    authentication_form = LoginForm

@method_decorator(login_required, name='dispatch')
class UserLogoutView(LogoutView):
    next_page = 'login'


@method_decorator(login_required, name='dispatch')
class MyPasswordChangeView(PasswordChangeView):
    template_name = 'app/changepassword.html'
    form_class = MyPasswordChangeForm
    success_url = '/profile/'


@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})

    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            urn = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=urn, name=name, locality=locality,
                           city=city, state=state, zipcode=zipcode)
            reg.save()
            return HttpResponseRedirect('/address/')
            if request.user.is_authenticated:
                totalitem = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary', 'totalitem': totalitem})
