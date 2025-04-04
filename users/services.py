# -*- coding: UTF-8 -*-
import os

import stripe
from django.core.mail import send_mail

from config.settings import STRIPE_API_KEY
from ed_platform.models import LessonModel, SubscriptionModel

stripe.api_key = STRIPE_API_KEY


def stripe_create_product(name, description):
    """Создаем продукт в Stripe"""
    product = stripe.Product.create(name=name, description=description)
    return product.get("name"), product.get("description")


def stripe_create_price(ammount):
    """Создает цену в stripe"""
    return stripe.Price.create(
        currency="rub",
        unit_amount=ammount * 100,
        product_data={"name": "Payment"},
    )


def stripe_create_session(price):
    """Создает сесиию в Stripe"""
    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")

def send_update(request):
    lesson_id = request.parser_context.get("kwargs").get(
        "pk"
    )  # Получаем id урока из запроса
    lesson = LessonModel.objects.get(id=lesson_id)
    course = lesson.course
    subscription = SubscriptionModel.objects.filter(course=course)
    recipient_list = list()
    for sub in subscription:
        recipient_list.append(sub.user)

    subject = "Обновился курс из ваших подписок!"
    message = f"В курсе \"{course.name}\" обновлен урок \"{lesson.name}\"!"
    from_email = os.getenv("EMAIL_HOST_USER")
    send_mail(subject, message, from_email, recipient_list)
