from decimal import Decimal

from django.conf import settings
from django.shortcuts import get_object_or_404

from ..models.item import Item


class Cart:
	"""
	The user's shopping cart.
	Implemented through sessions.
	"""

	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(settings.CART_SESSION_ID)
		if not cart:
			cart = self.session[settings.CART_SESSION_ID] = {}
		self.cart = cart

	def __iter__(self):
		product_ids = self.cart.keys()
		products = Item.objects.filter(id__in=product_ids)  # noqa
		for product in products:
			self.cart[str(product.id)]['product'] = product

		for item in self.cart.values():
			item['price'] = Decimal(item['price'])
			item['total_price'] = item['price'] * item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def add(self, product: Item, quantity=1, update_quantity=False):
		product_id = str(product.pk)
		if product_id not in self.cart:
			self.cart[product_id] = {
				'quantity': 0,
				'price': str(product.price)
			}
		if update_quantity:
			self.cart[product_id]['quantity'] = quantity
		else:
			self.cart[product_id]['quantity'] += quantity
		self.save()

	def remove(self, product: Item):
		product_id = str(product.pk)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def get_total_price(self):
		return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

	def save(self):
		self.session[settings.CART_SESSION_ID] = self.cart
		self.session.modified = True

	def clear(self):
		del self.session[settings.CART_SESSION_ID]
		self.session.modified = True


def cart_handler(request, pk: int, mode: bool = False) -> None:
	"""Adds or removes a product item"""
	cart = Cart(request)
	item = get_object_or_404(Item, pk=pk)
	if mode:
		cart.remove(item)
	else:
		cart.add(item)
