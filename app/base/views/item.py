from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from ..models.item import Item


class ItemView(TemplateView):
	"""Product page"""
	template_name = 'stripe/item.html'

	def get_context_data(self, **kwargs):
		context = super(ItemView, self).get_context_data(**kwargs)
		item_id = self.kwargs['pk']
		item = get_object_or_404(Item, pk=item_id)
		context.update({
			'item': item,
		})
		return context
