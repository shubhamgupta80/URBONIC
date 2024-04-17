from django.contrib import admin
from .models import Category, Contact, Product, Testimonial,Gallery

# Register your models here.
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Testimonial)
admin.site.register(Gallery)