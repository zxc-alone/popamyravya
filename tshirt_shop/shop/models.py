from django.db import models
from django.urls import reverse

class Category(models.Model):
    """Категория товаров"""
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Слаг', max_length=200, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    """Товар (футболка)"""
    SIZES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]
    
    COLORS = [
        ('white', 'Белый'),
        ('black', 'Черный'),
        ('red', 'Красный'),
        ('blue', 'Синий'),
        ('green', 'Зеленый'),
        ('yellow', 'Желтый'),
        ('gray', 'Серый'),
    ]
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория', related_name='products')
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('Слаг', max_length=200, unique=True)
    description = models.TextField('Описание', blank=True)
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)
    size = models.CharField('Размер', max_length=3, choices=SIZES, default='M')
    color = models.CharField('Цвет', max_length=10, choices=COLORS, default='white')
    image = models.ImageField('Изображение', upload_to='products/%Y/%m/%d', blank=True, null=True)
    available = models.BooleanField('Доступен', default=True)
    created = models.DateTimeField('Создан', auto_now_add=True)
    updated = models.DateTimeField('Обновлен', auto_now=True)

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created']

    def __str__(self):
        return f"{self.name} ({self.get_size_display()}, {self.get_color_display()})"

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])