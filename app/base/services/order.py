from ..models.cart import Order, OrderItem
from ..models.item import Item
from ..services.cart import Cart


def create_order(item: Item, session_id: str) -> None:
	"""Creates an order for one product"""
	new_order = Order(
		order_id=session_id,
		amount=item.price
	)
	new_order.save()
	new_order_item = OrderItem(
		item=item,
		order=new_order,
		quantity=1,
		amount=item.price
	)
	new_order_item.save()


def create_group_order(items: Cart, session_id) -> None:
	"""Creates an order for a product group"""
	new_order = Order(
		order_id=session_id,
		amount=items.get_total_price()
	)
	new_order.save()
	for item in items:
		new_order_item = OrderItem(
			item=item['product'],
			order=new_order,
			quantity=item['quantity'],
			amount=(item['price'] * item['quantity'])
		)
		new_order_item.save()
