from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from ..services.payment import create_stripe_session, create_stripe_payment_intents, create_item_list
from ..services.webhook import stripe_webhook


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebHook(View):
	def post(self, *args, **kwargs):
		return stripe_webhook(self.request)


class StripeIntentView(TemplateView):
	"""Product payment page using StipeIntent"""
	template_name = 'stripe/intent.html'

	def post(self, request, *args, **kwargs):
		response = create_stripe_payment_intents(self.kwargs["pk"])
		return JsonResponse(response)


class CreateCheckoutSessionView(View):
	"""Product payment page using Stipe Session"""

	def get(self, request, *args, **kwargs):
		result = create_stripe_session(self.kwargs['pk'])
		return JsonResponse({'session_id': result.get('session_id')})

	def post(self, request, *args, **kwargs):
		result = create_stripe_session(self.kwargs['pk'])
		return redirect(result.get('session_url'))


class CreateCheckoutCartView(View):
	"""Creating a shopping list and processing a payment"""

	def get(self, request, *args, **kwargs):
		return redirect(create_item_list(request))


class SuccessView(TemplateView):
	template_name = "stripe/success.html"


class CancelView(TemplateView):
	template_name = "stripe/cancel.html"
