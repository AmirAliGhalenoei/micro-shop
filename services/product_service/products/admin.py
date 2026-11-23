from django.contrib import admin

from .models import Category, Product, GaleryProducts
# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    list_filter = ["is_sub"]


class GaleryInlines(admin.TabularInline):
    model = GaleryProducts
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [GaleryInlines]
    list_display = ["name"]
