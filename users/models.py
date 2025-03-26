from django.contrib.auth.models import AbstractUser
from django.db import models

from ed_platform.models import CourseModel, LessonModel


class CustomUser(AbstractUser):

    email = models.EmailField(unique=True, verbose_name="Email")
    avatar = models.ImageField(upload_to="users/avatars/", verbose_name="Аватар", null=True, blank=True)
    phone = models.CharField(max_length=35, verbose_name="Phone", null=True, blank=True,
                             help_text="Введите номер телефона")
    country = models.CharField(max_length=50, verbose_name="Страна", help_text="Введите страну")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username",]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class PaymentModel(models.Model):
    CASH = 'Наличные'
    NON_CASH = 'Перевод'

    PAYMENT_IN_CHOICES = [
        (CASH, 'Наличные'),
        (NON_CASH, 'Перевод')
    ]

    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True, verbose_name='студент', related_name='student')
    payment_date = models.DateTimeField(verbose_name='дата оплаты')
    paid_course = models.ForeignKey(CourseModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='оплаченный курс', related_name='paid_course')
    paid_lesson = models.ForeignKey(LessonModel, on_delete=models.CASCADE, blank=True, null=True, verbose_name='оплаченный урок', related_name='paid_lesson')
    cost = models.PositiveIntegerField(verbose_name='стоимость')
    payment_type = models.CharField(choices=PAYMENT_IN_CHOICES, verbose_name='способ оплаты')

    def __str__(self):
        return f'{self.paid_course if self.paid_course else self.paid_lesson}'

    class Meta:
        verbose_name = 'оплата'
        verbose_name_plural = 'оплата'