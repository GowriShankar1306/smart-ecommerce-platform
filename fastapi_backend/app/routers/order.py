from fastapi import APIRouter, Depends, HTTPException, status
from app.models import order
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app.schemas.order import OrderResponse
from app.routers.auth import require_customer
from app.models.notification import Notification
from app.services.email_service import send_order_confirmation_email
from app.services.websocket_manager import manager

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post(
    "/",
    response_model=OrderResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_order(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_customer)
):
    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user["user_id"]
    ).all()

    if not cart_items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cart is empty"
        )

    total = 0

    for cart_item in cart_items:
        product = db.query(Product).filter(
            Product.id == cart_item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {cart_item.product_id} not found"
            )

        if product.stock < cart_item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )

        total += float(product.price) * cart_item.quantity

    order = Order(
        user_id=current_user["user_id"],
        total=total,
        payment_status="pending",
        order_status="pending"
    )

    db.add(order)
    db.flush()

    for cart_item in cart_items:
        product = db.query(Product).filter(
            Product.id == cart_item.product_id
        ).first()

        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=cart_item.quantity,
            price=product.price
        )

        db.add(order_item)

        product.stock -= cart_item.quantity

        db.delete(cart_item)
    notification = Notification(
        user_id=current_user["user_id"],
        type="order_confirmation",
        message=f"Your order #{order.id} has been confirmed.",
        is_read=False,
    )

    db.add(notification)

    db.commit()
    db.refresh(order)

    await manager.send_notification(
        user_id=current_user["user_id"],
        message=f"Your order #{order.id} has been confirmed."
    )
    await send_order_confirmation_email(
        recipient_email=current_user["email"],
        order_id=order.id,
        amount=float(order.total),
   )

    return order 


@router.get(
    "/",
    response_model=list[OrderResponse]
)
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_customer)
):
    orders = db.query(Order).filter(
        Order.user_id == current_user["user_id"]
    ).order_by(
        Order.timestamp.desc()
    ).all()

    return orders


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_customer)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user["user_id"]
    ).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return order