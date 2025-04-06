# -*- coding: UTF-8 -*-

import stripe

from config.settings import STRIPE_API_KEY

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
