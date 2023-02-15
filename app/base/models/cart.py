import datetime

from django.db import models

from .item import Item

ORDER_CHOICES = [
	('UP', 'Unpaid'),
	('PA', 'Paid'),
]


class Order(models.Model):
	"""User shopping cart"""
	order_id = models.CharField(max_length=255, db_index=True)
	date = models.DateTimeField(default=datetime.datetime.now)
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	status = models.CharField(max_length=25, choices=ORDER_CHOICES, default='UP')

	def __str__(self):
		return self.order_id

	class Meta:
		db_table = 'order'


class OrderItem(models.Model):
	"""Products attached to the order"""
	item = models.ForeignKey(Item, on_delete=models.PROTECT, related_name='items')
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
	quantity = models.PositiveSmallIntegerField(default=1)
	amount = models.DecimalField(max_digits=5, decimal_places=2)

	def __str__(self):
		return self.item.name

	class Meta:
		db_table = 'order_item'

# TODO
# class Discount(models.Model):
# 	pass
#
#
# class Tax(models.Model):
# 	pass
