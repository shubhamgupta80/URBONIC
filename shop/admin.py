from django.contrib import admin
from .models import Category, Contact, Product, Testimonial,Gallery, Review, Article, ArticleVote, Order, OrderItem

# Register your models here.
admin.site.register(Category)
admin.site.register(Contact)
admin.site.register(Product)
admin.site.register(Testimonial)
admin.site.register(Gallery)
admin.site.register(Review)
admin.site.register(Article)
admin.site.register(ArticleVote)
admin.site.register(Order)
admin.site.register(OrderItem)