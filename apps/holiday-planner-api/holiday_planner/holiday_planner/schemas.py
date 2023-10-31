# schemas.py
from djantic import ModelSchema

from orders.models import OrderItemDetail, OrderItem, Order, OrderUserProfile


class OrderItemDetailSchema(ModelSchema):
    class Config:
        model = OrderItemDetail

class OrderItemSchema(ModelSchema):
    details: List[OrderItemDetailSchema]

    class Config:
        model = OrderItem

class OrderSchema(ModelSchema):
    items: List[OrderItemSchema]

    class Config:
        model = Order

class OrderUserProfileSchema(ModelSchema):
    class Config:
        model = OrderUserProfile

class OrderUserSchema(ModelSchema):
    orders: List[OrderSchema]
    profile: OrderUserProfileSchema
