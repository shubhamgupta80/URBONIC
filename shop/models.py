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
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    best_seller = models.BooleanField(default=False)
    seller = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.title
    
class Testimonial(models.Model):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='Product')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.title
    
class Gallery(models.Model):
    image = models.ImageField(upload_to='Product')
    created_at = models.DateTimeField(auto_now_add=True)
    


    def __str__(self):
        return self.created_at