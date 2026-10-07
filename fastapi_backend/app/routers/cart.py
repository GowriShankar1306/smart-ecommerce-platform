from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.cart import Cart
from app.models.product import Product
from app.schemas.cart import CartAdd, CartUpdate, CartResponse
from app.routers.auth import require_customer


router = APIRouter(
    prefix="/cart",
    tags=["Cart"]
)


@router.post(
    "/",
    response_model=CartResponse,
    status_code=status.HTTP_201_CREATED
)
def add_to_cart(
    cart_data: CartAdd,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_customer)
):
    product = db.query(Product).filter(
        Product.id == cart_data.product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.stock < cart_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient product stock"
        )

    existing_cart = db.query(Cart).filter(
        Cart.user_id == current_user["user_id"],
        Cart.product_id == cart_data.product_id
    ).first()

    if existing_cart:
        new_quantity = existing_cart.quantity + cart_data.quantity

        if product.stock < new_quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Insufficient product stock"
            )

        existing_cart.quantity = new_quantity
        db.commit()
        db.refresh(existing_cart)

        return existing_cart

    cart_item = Cart(
        user_id=current_user["user_id"],
        product_id=cart_data.product_id,
        quantity=cart_data.quantity
    )

    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)

    return cart_item

@router.get(
    "/",
    response_model=list[CartResponse]
)
def get_my_cart(
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_customer)
):
    cart_items = db.query(Cart).filter(
        Cart.user_id == current_user["user_id"]
    ).all()

    return cart_items


@router.put(
    "/{product_id}",
    response_model=CartResponse
)
def update_cart(
    product_id: int,
    cart_data: CartUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_customer)
):
    cart_item = db.query(Cart).filter(
        Cart.user_id == current_user["user_id"],
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in cart"
        )

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    if product.stock < cart_data.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient product stock"
        )

    cart_item.quantity = cart_data.quantity

    db.commit()
    db.refresh(cart_item)

    return cart_item

@router.delete("/{product_id}")
def remove_from_cart(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_customer)
):
    cart_item = db.query(Cart).filter(
        Cart.user_id == current_user["user_id"],
        Cart.product_id == product_id
    ).first()

    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found in cart"
        )

    db.delete(cart_item)
    db.commit()

    return {
        "message": "Product removed from cart successfully"
    }