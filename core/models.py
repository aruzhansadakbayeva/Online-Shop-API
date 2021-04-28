from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

PRODUCT_TYPE_CLOTHES = 1
PRODUCT_TYPE_ACCESSORIES = 2
PRODUCT_TYPES = (
    (PRODUCT_TYPE_CLOTHES, 'clothes'),
    (PRODUCT_TYPE_ACCESSORIES, 'accessories')
)

ORDER_STATUS_IN_PROCESS = 1
ORDER_STATUS_DONE = 2
ORDER_STATUS_CANCELED = 3
ORDER_STATUSES = (
    (ORDER_STATUS_IN_PROCESS, 'in process'),
    (ORDER_STATUS_DONE, 'done'),
    (ORDER_STATUS_CANCELED, 'canceled')
)


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=100)
    type = models.SmallIntegerField(choices=PRODUCT_TYPES,
                                    default=PRODUCT_TYPE_CLOTHES,
                                    verbose_name='Вид продукта')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название продукта')
    price = models.FloatField(verbose_name='Цена')
    short_description = models.TextField(blank=True, null=True, verbose_name='Краткое описание продукта')
    in_stock = models.BooleanField(default=False, verbose_name='Есть в наличие?')
    long_description = models.TextField(blank=True, null=True, verbose_name='Полное описание продукта')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='products',
                                 verbose_name='Категория')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name} {self.price}'


class ProductImage(models.Model):
    src = models.ImageField(upload_to='images/products', verbose_name='Картинки')
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                verbose_name='Продукт',
                                related_name='images',
                                blank=True,
                                null=True)


class Meta:
    verbose_name = 'Картинка продукта'
    verbose_name_plural = 'Картинки продукта'


class UserShoppingCart(models.Model):
    owner = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 verbose_name='Владелец корзины',
                                 related_name='cart',
                                 blank=True,
                                 null=True)

    class Meta:
        verbose_name = 'Корзина пользователя'

    @property
    def total_price(self):
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total


class CartItem(models.Model):
    product = models.ForeignKey(Product,
                                on_delete=models.CASCADE,
                                related_name='carts',
                                verbose_name='Продукт')
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(UserShoppingCart,
                             on_delete=models.CASCADE,
                             related_name='items',
                             verbose_name='Корзина',
                             blank=True,
                             null=True)

    class Meta:
        verbose_name = 'Запись корзины'
        verbose_name_plural = 'Записи корзины'

    @property
    def total_price(self):
        return self.product.price * self.quantity


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(blank=True, null=True, max_length=20)


@receiver(post_save, sender=User)
def create_user_shopping_cart(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserShoppingCart.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
