from django.db import models
from django.conf import settings
from django.shortcuts import reverse

# Create your models here.


Quantity_Choices = (
    ("k", "KG"),
    ("l", "Ltrs"),
    ("d", "Dozens"),
    ("u", "Units")
)

class Category(models.Model):
    category = models.CharField(max_length=30)
    img = models.ImageField(upload_to='pics')
    slug = models.SlugField()
    
    def __str__(self):
        return self.category
    
    def get_absolute_url(self):
        return reverse("home:category", kwargs={
            'slug': self.slug
        })

class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.CharField(max_length = 100)
    def __str__(self):
        return self.sub_category
        
class Item(models.Model):
    title = models.CharField(max_length = 100)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='pics')
    description = models.TextField()
    measured_by = models.CharField(choices=Quantity_Choices, max_length=1)
    slug = models.SlugField()
    
    def __str__(self):
        return self.title

class Price(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    kkd_rural_p = models.FloatField(blank=True, null=True)
    kkd_urban_p = models.FloatField(blank=True, null=True)
    
    kkd_rural_dp = models.FloatField(blank=True, null=True)
    kkd_urban_dp = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return self.item.title
    
    
    
class OrderItem(models.Model):
    item = models.ForeignKey(Price, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    ordered = models.BooleanField(default = False)
    quantity = models.FloatField(default = 1)
    price = models.FloatField(blank=True, null=True)
    discounted_price = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.item.item.title
    def get_total_discount_item_price(self):
        return self.discounted_price*self.quantity
    def get_amount_saved(self):
        return (self.price- self.discounted_price)*self.quantity
    def get_total_item_price(self):
        return self.price*self.quantity
    
    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    order_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default = False)
    total_amount = models.FloatField(blank=True, null=True)
    amount_saved = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.user.name
    def get_total(self):
        return self.total_amount
    def get_saved(self):
        return self.amount_saved
    