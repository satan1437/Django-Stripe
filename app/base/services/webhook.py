import stripe
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from stripe.error import SignatureVerificationError

from ..models.cart import Order


def stripe_webhook(request: WSGIRequest) -> HttpResponse | None:
	payload = request.body
	sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
	event = None

	try:
		event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
	except (ValueError, SignatureVerificationError) as ex:  # FIXME
		return HttpResponse(status=400)

	if event.get('type') == 'checkout.session.completed':  # TODO: make business logic
		if event['data']['object']['payment_status'] == 'paid':
			data = event['data']['object']
			try:
				order = Order.objects.get(order_id=data['id'])  # noqa
				order.status = 'PA'
				order.save()
			except ObjectDoesNotExist as ex:  # FIXME: create logic
				pass
	elif event.get('type') == "payment_intent.succeeded":  # TODO: make business logic
		intent = event['data']['object']
		# сan get a customer
		# stripe_customer_id = intent["customer"]
		# stripe_customer = stripe.Customer.retrieve(stripe_customer_id)
		try:
			order = Order.objects.get(order_id=intent['id'])  # noqa
			order.status = 'PA'
			order.save()
		except ObjectDoesNotExist as ex:  # FIXME: create logic
			pass
	return HttpResponse(status=200)
