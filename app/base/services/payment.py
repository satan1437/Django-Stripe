import stripe
from django.conf import settings
from django.urls import reverse_lazy

from .order import create_order, create_group_order
from ..models.item import Item
from ..services.cart import Cart

stripe.api_key = settings.STRIPE_SECRET_KEY
IMAGE = ['https://i.imgur.com/EHyR2nP.png']  # FIXME


def create_stripe_payment_intents(pk):
	"""PaymentIntents"""
	try:
		customer = stripe.Customer.create()
		product = Item.objects.get(id=pk)  # noqa
		intent = stripe.PaymentIntent.create(
			amount=int(product.price * 100),
			currency='usd',
			customer=customer['id'],
			metadata={
				"product_id": product.id,
				"item": product.name
			}
		)
		create_order(product, intent['id'])  # FIXME: each request = new order (see stripe_checkout.js)
		return {'clientSecret': intent['client_secret']}
	except Exception as e:
		return {'error': str(e)}


def create_stripe_session(pk):  # TODO: make handler for exemptions
	"""Checkout Session"""
	product = Item.objects.get(id=pk)  # noqa
	checkout_session = stripe.checkout.Session.create(  # TODO: create metadata
		payment_method_types=['card'],
		line_items=[  # FIXME: DRY
			{
				'price_data': {
					'currency': 'usd',
					'unit_amount': int(product.price * 100),
					'product_data': {
						'name': product.name,
						'description': product.description,
						'images': IMAGE
					},
				},
				'quantity': 1,
			}
		],
		metadata={
			'product_id': product.pk,
		},
		mode='payment',
		success_url=settings.SUCCESS_URL,
		cancel_url=settings.CANCEL_URL,
	)
	create_order(product, checkout_session.id)
	return {'session_id': checkout_session.id, 'session_url': checkout_session.get('url')}


def create_group_stripe_session(list_items, items):
	"""Checkout Session"""
	if not list_items:
		return reverse_lazy('cart')
	checkout_session = stripe.checkout.Session.create(
		payment_method_types=['card'],
		line_items=list_items,  # FIXME: DRY
		mode='payment',
		success_url=settings.SUCCESS_URL,
		cancel_url=settings.CANCEL_URL,
	)
	create_group_order(items, checkout_session.id)
	return checkout_session.get('url')


def create_item_list(request):
	"""Creates and returns a list of items to buy"""
	items = Cart(request)
	line_items = []
	for item in items:
		product = {
			'price_data': {
				'currency': 'usd',
				'unit_amount': int(item['price'] * 100),  # FIXME
				'product_data': {
					'name': item['product'].name,
					'description': item['product'].description,
					'images': IMAGE
				},
			},
			'quantity': item['quantity'],
		}
		line_items.append(product)
	items.clear()  # TODO: check the success of the transaction
	return create_group_stripe_session(line_items, items)
