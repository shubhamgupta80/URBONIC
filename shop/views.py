from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ReviewForm
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout

def home_view(request):
    articles = Article.objects.all()[:3]
    products = Product.objects.all()[:9]
    return render(request, 'index.html', {'articles': articles, 'products': products})


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
    return redirect('vendor_login')

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