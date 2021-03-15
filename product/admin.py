from django.contrib import admin

from .models import Category, Product, Image


class CategoryAdmin(admin.ModelAdmin):
    exclude = ('slug', )
    list_display = ('title', 'slug')
    list_display_links = ('title', )

class ProductImagesInline(admin.TabularInline):
    model = Image
    fields = ['image', ]

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesInline, ]
    list_display = ['id', 'title', 'price']
    list_display_links = ['id', 'title']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)




