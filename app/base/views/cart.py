from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView

from ..models.item import Item
from ..services.cart import Cart, cart_handler


class ShowCartView(ListView):
	"""Page with the user's shopping cart"""
	model = Item
	template_name = 'stripe/cart.html'
	context_object_name = 'my_cart'

	def get_queryset(self):
		return Cart(self.request)


class AddItemCartView(View):  # TODO: XHR

	def get(self, request, *args, **kwargs):  # maybe POST?
		cart_handler(request, self.kwargs['pk'])
		return redirect('cart')


class RemoveItemCartView(View):  # TODO: XHR

	def get(self, request, *args, **kwargs):
		cart_handler(request, self.kwargs['pk'], mode=True)
		return redirect('cart')
