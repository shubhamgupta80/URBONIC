# urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from shop.views import *

urlpatterns =[
    path('adminn/', admin.site.urls),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    path('', home_view, name='home'),
    path('page', TemplateView.as_view(template_name='page1.html'), name='page1'),
    path('pricing', TemplateView.as_view(template_name='pricing.html'), name='pricing'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('review', review_view, name='review'),
    path('login', user_login_view, name='login'),
    path('register', user_register_view, name='register'),
    path('vendor/login',vendor_login_view, name='vendor_login'),
    path('vendor/register', vendor_register_view, name='vendor_register'),
    path('logout', logout_view, name='logout'),
    path('contact', contact_view , name='contact'),
    path('products/all', product_view, name="products"),
    path('article/<int:pk>',article_view , name="article"),
    path('article/all', article_all_view, name="articles"),
    path('checkout', checkout_view, name='checkout'),

    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)