from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Item(models.Model):
	"""Item to buy"""
	name = models.CharField(max_length=255)
	description = models.TextField()
	price = models.DecimalField(
		max_digits=5,
		decimal_places=2,
		validators=[
			MinValueValidator(0.50),  # stripe limit
			MaxValueValidator(999),
		])

	def __str__(self):
		return self.name

	class Meta:
		db_table = 'item'
