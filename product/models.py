
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()


class Category(models.Model):
    title = models.TextField(max_length=100)
    slug = models.SlugField(primary_key=True, unique=True, max_length=100, blank=True)

    def save(self, *args, **kwargs):
        self.slug = self.title.lower()
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Product(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    name = models.CharField(max_length=100, unique=True)
    amount = models.PositiveIntegerField(default=1)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

class Rating(models.Model):
    """Модель для рейтинга"""

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', verbose_name='Пользователь рейтинга')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings', verbose_name='Названия продукта')
    rating = models.SmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ],default=1
    )

    def __str__(self):
        return f'{self.product} - {self.rating}'



class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment for {self.product}'



class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='Владелец лайка')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes', verbose_name='Товар')
    like = models.BooleanField('лайк', default=False)

    def __str__(self):
        return f'{self.product} {self.like}'


class Image(models.Model):

    image = models.ImageField(upload_to='product')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

