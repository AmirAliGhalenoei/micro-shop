from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80, unique=True)
    sub = models.ForeignKey(
        "self", 
        on_delete=models.CASCADE, 
        related_name="sub_categorys", 
        null=True, blank=True
    )
    is_sub = models.BooleanField(default=False)

    def __str__(self):
            return self.name

class Product(models.Model):
    category = models.ManyToManyField(Category, related_name="products")
    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=80, unique=True)
    baner = models.ImageField(upload_to=f"product_baners/")
    caption = models.TextField()
    price = models.BigIntegerField()
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)], 
        null=True, 
        blank=True
    )
    is_available = models.BooleanField(default=True)
    discounted = models.BooleanField(default=False)


    def total_amount(self):
        price = self.price
        if self.discount:
            price = price * (1 - self.discount / 100)
        return price

    def __str__(self):
        return self.name

class GaleryProducts(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="galerys")
    image = models.ImageField(upload_to=f"galareys/")
