from django.db import models
from django.urls import reverse_lazy
from pytils.translit import slugify

from account.models import User


class Category(models.Model):
    slug = models.SlugField(primary_key=True, max_length=50)
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories', blank=True, null=True)

    def __str__(self):
       return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Product(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

    @property
    def get_image(self):
        return self.images.first()

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('detail', kwargs={'pk': self.pk})


class Image(models.Model):
    image = models.ImageField(upload_to='products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        if self.image:
            return self.image.url
        return ''


class Comments(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()

    def get_absolute_url(self):
        return reverse_lazy("product-detail.html", args=[str(self.pk)])

    # class Cart(models.Model):
    #     owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    #     products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    #     total_products = models.PositiveIntegerField(default=0)
    #     final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    #     in_order = models.BooleanField(default=False)
    #     for_anonymous_user = models.BooleanField(default=False)
    #
    #     def __str__(self):
    #         return str(self.id)
