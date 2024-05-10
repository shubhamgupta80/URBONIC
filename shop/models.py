from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    image = models.ImageField(upload_to='category')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class Contact(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Product')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    best_seller = models.BooleanField(default=False)
    seller = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
            return self.title
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    description = models.TextField(default='Awesome Product')
    rating = models.IntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Testimonial(models.Model):
    description = models.TextField()
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.description
    
class Gallery(models.Model):
    image = models.ImageField(upload_to='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.image.url
    

from django_ckeditor_5.fields import CKEditor5Field

class Article(models.Model):
    title=models.CharField('Title', max_length=200)
    image = models.ImageField(upload_to='article', default="logo1.png")
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    text=CKEditor5Field('Text', config_name='extends')

class ArticleVote(models.Model):
    vote_choices = (
        (1, 'Like'),
        (-1, 'Dislike')
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    value = models.SmallIntegerField(choices=vote_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('article', 'user')