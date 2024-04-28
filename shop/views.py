from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ReviewForm
from .models import *
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required



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

