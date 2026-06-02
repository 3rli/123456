from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db.models import Sum, Avg, Count, F

class PlantManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()

    def available(self):
        return self.get_queryset().filter(is_in_stock=True)

class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг (URL)')
    source_url = models.URLField(blank=True, verbose_name='Ссылка на описание (URL)')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

class Plant(models.Model):
    category = models.ForeignKey(Category, related_name='plants', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField(max_length=200, verbose_name='Название растения')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    is_in_stock = models.BooleanField(default=True, verbose_name='В наличии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    published_at = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')

    image = models.ImageField(upload_to='plants/%Y/%m/%d', blank=True, verbose_name='Изображение')
    manual = models.FileField(upload_to='manuals/%Y/%m/%d', blank=True, verbose_name='Инструкция по уходу (PDF)')
    tags = models.ManyToManyField('Tag', blank=True, related_name='plants', verbose_name='Теги')
    
    objects = models.Manager()
    available_plants = PlantManager()

    class Meta:
        ordering = ('name',)
        verbose_name = 'Растение'
        verbose_name_plural = 'Растения'
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:plant_detail', args=[self.id, self.slug])

    def get_discount_price(self, discount=10):
        return self.price * (1 - discount / 100)


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')
    content = models.TextField(verbose_name='Контент')
    author = models.CharField(max_length=100, verbose_name='Автор')
    published_at = models.DateTimeField(default=timezone.now, verbose_name='Дата публикации')
    image = models.ImageField(upload_to='articles/%Y/%m/%d', blank=True, verbose_name='Изображение')
    is_active = models.BooleanField(default=True, verbose_name='Активна')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    plants = models.ManyToManyField(Plant, blank=True, related_name='articles', verbose_name='Связанные растения')

    class Meta:
        ordering = ('-published_at',)
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'

    def __str__(self):
        return self.title


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', 'В ожидании'
        PROCESSING = 'PR', 'В обработке'
        SHIPPED = 'S', 'Отправлено'
        DELIVERED = 'D', 'Доставлено'
        CANCELLED = 'C', 'Отменено'

    customer_name = models.CharField(max_length=100, verbose_name='Имя клиента')
    customer_email = models.EmailField(verbose_name='Email клиента')
    phone = models.CharField(max_length=20, verbose_name='Телефон', blank=True)
    address = models.CharField(max_length=250, verbose_name='Адрес', blank=True)
    city = models.CharField(max_length=100, verbose_name='Город', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    status = models.CharField(
        max_length=2, 
        choices=Status.choices, 
        default=Status.PENDING, 
        verbose_name='Статус'
    )

    delivery_date = models.DateField(null=True, blank=True, verbose_name='Дата доставки')
    
    plants = models.ManyToManyField(
        Plant, 
        through='OrderItem', 
        related_name='orders',
        verbose_name='Растения в заказе'
    )

    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='Заказ')
    plant = models.ForeignKey(Plant, related_name='order_items', on_delete=models.CASCADE, verbose_name='Растение')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'

    def __str__(self):
        return f'Позиция {self.id}'

    def get_cost(self):
        return self.price * self.quantity


class Cart(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='cart', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f'Корзина {self.user.username}'

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE, verbose_name='Корзина')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, verbose_name='Растение')
    quantity = models.PositiveIntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def __str__(self):
        return f'{self.plant.name} (x{self.quantity})'

    def get_cost(self):
        return self.plant.price * self.quantity
