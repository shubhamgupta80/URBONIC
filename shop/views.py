from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ReviewForm
from .models import *
from .models import Gallery
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import dotenv
import stripe
import os
from django.conf import settings
import json
from django.core.mail import send_mail


from django.http import JsonResponse
@csrf_exempt
@login_required
def create_checkout_session(request):
    # clear session
    request.session['prod_ids'] = []
    # grab json data from the request
    data = json.loads(request.body)
    print(data)
    base_url = request.build_absolute_uri('/')[:-1]
    stripe.api_key = settings.STRIPE_SECRET_KEY
    print(stripe.api_key)
    YOUR_DOMAIN = base_url
    user = request.user
    print(user)
    totalPrice = data.get('totalPrice')
    qty = data.get('totalQuantity',1)
    prod_ids = []
    for item in data.get('items'):
        prod_ids.append(item.get('id'))
    # store ids in session
    request.session['prod_ids'] = prod_ids
    request.session['totalPrice'] = totalPrice
    request.session['qty'] = qty
    request.session['phone'] = data.get('phone')
    request.session['address'] = data.get('address')   
    request.session['city'] = data.get('city')
    request.session['country'] = data.get('country')
    currency = 'inr'
    # create a checkout session
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        mode='payment',
        success_url=f'{base_url}/success/',
        cancel_url=f'{base_url}/cancel/',
        # customer name and info
        line_items=[
            {
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'URBONIC Products',
                    },
                    'unit_amount': int(totalPrice*100),
                },
                'quantity': 1,
            },
        ],
        customer_email= user.email,
        billing_address_collection='required',
    )
    return JsonResponse({'sessionId': checkout_session.id})

def success_view(request):
    prod_ids = request.session.get('prod_ids')
    products = Product.objects.filter(id__in=prod_ids)
    totalPrice = request.session.get('totalPrice')
    qty = request.session.get('qty')
    phone = request.session.get('phone')
    address = request.session.get('address')
    city = request.session.get('city')
    country = request.session.get('country')

    order = Order(
        user=request.user,
        amount=totalPrice,
        phone=phone,
        address=address,
        city=city,
        country=country
    )
    order.save()
    # create a new order item
    for prod_id in prod_ids:
        product = Product.objects.get(id=prod_id)
        order_item = OrderItem(
            order=order,
            product=product,
            quantity=qty,
            price=product.price
        )
        order_item.save()
    
    return render(request, 'success.html', {
        'products': products,
        'totalPrice': totalPrice,
        'qty': qty,
        'phone': phone,
        'address': address,
        'city': city,
        'country': country
    })

def cancel_view(request):
    # clear session
    clear_order_sesion(request)
    return render(request, 'cancel.html')

def clear_order_sesion(request):
    request.session['prod_ids'] = []
    request.session['totalPrice'] = 0
    request.session['qty'] = 0
    request.session['phone'] = ''
    request.session['address'] = ''
    request.session['city'] = ''
    request.session['country'] = '' 

def home_view(request):
    articles = Article.objects.all()[:3]
    products = Product.objects.all()[:9]
    return render(request, 'index.html', {'articles': articles, 'products': products})

def gallery_view(request):
    gallery= Gallery.objects.all()
    return render(request, 'gallery.html', {'gallery': gallery})
    




# Create your views here.
def contact_view(request):
    if request.method == 'POST':
        # extract info from the form
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        if len(name)> 0 and len(email)> 0 and len(subject)> 0 and len(message)> 0:
            # save the data to the database
            contact = Contact(name=name, email=email, subject=subject, message=message)
            contact.save()
            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all the fields!")
    return render(request, 'contact.html')

@login_required
def review_view(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, )
        if form.is_valid():
            model = form.save()
            model.user = request.user
            model.save()
            messages.success(request, "Your review has been submitted successfully!")
            return redirect('review')
    else:
        form = ReviewForm()
    return render(request, 'reviewform.html', {'form': form})

# vendor login
def vendor_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if len(username) > 0 and len(password) > 0:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.groups.filter(name='vendor').exists():
                    login(request, user)
                    messages.success(request, "You have logged in successfully!")
                    return redirect('vendor_login')
                else:
                    messages.error(request, "You are not a vendor!")
            else:
                messages.error(request, "Invalid username or password!")
    return render(request, 'vendor_login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def user_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if len(username) > 0 and len(password) > 0:
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.groups.filter(name='user').exists():
                    login(request, user)
                messages.success(request, "You have logged in successfully!")
                return redirect('home')
            else:
                messages.error(request, "Invalid username or password!")
    return render(request, 'login.html')


def user_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(username) > 0 and len(email) > 0 and len(password) > 0:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                group = Group.objects.get(name='user')
                user.groups.add(group)
                messages.success(request, "You have registered successfully!")
                return redirect('login')
        else:
            messages.error(request, "Please fill in all the fields!")
    return render(request, 'register.html')

def vendor_register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if len(username) > 0 and len(email) > 0 and len(password) > 0:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists!")
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                group = Group.objects.get(name='vendor')
                user.groups.add(group)
                messages.success(request, "You have registered successfully!")
                return redirect('vendor_login')
        else:
            messages.error(request, "Please fill in all the fields!")
    return render(request, 'vendor_register.html')

def product_view(request):
    products = Product.objects.all()   
    return render(request, 'products.html', {'products': products}) 

def article_view(request, pk):
    article = Article.objects.get(pk=pk)
    return render(request, 'article.html', {'article': article})

def article_all_view(request):
    articles = Article.objects.all()
    print(len(articles))
    return render(request, "articles.html", {
        'articles' : articles
    })

@login_required
def checkout_view(request):
    return render(request, 'checkout.html', {
        'stripe_pk': settings.STRIPE_PUBLIC_KEY
    })