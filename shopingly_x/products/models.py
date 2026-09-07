from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products',
                                  on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/', blank=True, null=True)
    image_url = models.URLField(blank=True, help_text='Fallback image URL if no file uploaded')

    price = models.DecimalField(max_digits=10, decimal_places=2,
                                 help_text='Original / MRP price')
    offer_price = models.DecimalField(max_digits=10, decimal_places=2,
                                       blank=True, null=True,
                                       help_text='Discounted price shown to customers. Leave blank if no offer.')

    stock = models.PositiveIntegerField(default=10)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['id', 'slug'])]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('products:product_detail', args=[self.id, self.slug])

    @property
    def current_price(self):
        """The price to actually charge: offer price if set, else regular price."""
        return self.offer_price if self.offer_price else self.price

    @property
    def discount_percent(self):
        if self.offer_price and self.price > 0:
            return round((1 - (self.offer_price / self.price)) * 100)
        return 0

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return ''
