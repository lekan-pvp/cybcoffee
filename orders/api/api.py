import time
from datetime import datetime
import uuid
from uuid import UUID

from fastapi import HTTPException
from starlette.responses import Response
from starlette import status

from orders.app import app
from orders.api.schemas import (
    GetOrderSchema,
    CreateOrderSchema,
    GetOrdersSchema,
)

orders = []

o_id = uuid.uuid4()

order = {
    'id': o_id,
    'status': 'delivered',
    'created': datetime.now(),
    'order': [
        {
            'product': 'cappuccino',
            'size': 'medium',
            'quantity': 1
        }
    ]
}

@app.get('/orders', response_model=GetOrdersSchema)
def get_orders():
    return {'orders': [order]}

@app.post(
    '/orders', 
    status_code=status.HTTP_201_CREATED,
    response_model=GetOrderSchema,
)
def create_order(order_details: CreateOrderSchema):
    order = order_details.model_dump()
    order["id"] = uuid.uuid4()
    order["created"] = datetime.now()
    order["status"] = "created"
    orders.append(order)
    return order

@app.get('/orders/{order_id}', response_model=GetOrderSchema)
def get_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order.upadate(order_details.model_dump())
            return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

@app.put('/orders/{order_id}', response_model=GetOrderSchema)
def update_order(order_id: UUID, order_details: CreateOrderSchema):
    for index, order in orders:
        if order["id"] in enumerate(orders):
            orders.pop(index)
            return
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

@app.delete(
    '/orders/{order_id}', 
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_order(order_id: UUID):
    for index, order in enumerate(orders):
        if order["id"] == order_id:
            orders.pop(index)
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

@app.post('/orders/{order_id}/cancel', response_model=GetOrderSchema)
def cancel_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "cancelled"
            return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")

@app.post('/orders/{order_id}/pay', response_model=GetOrderSchema)
def pay_order(order_id: UUID):
    for order in orders:
        if order["id"] == order_id:
            order["status"] = "progress"
            return order
    raise HTTPException(status_code=404, detail=f"Order with ID {order_id} not found")
