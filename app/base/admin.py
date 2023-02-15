from django.contrib import admin

from .models import Item, Order, OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	list_display = ('name', 'description', 'price')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('item', 'order', 'quantity', 'amount')
	readonly_fields = ('item', 'order')


class OrderItemInline(admin.TabularInline):
	model = OrderItem
	extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ('order_id', 'date', 'amount', 'status')
	readonly_fields = ('order_id', 'date')
	inlines = [OrderItemInline]
