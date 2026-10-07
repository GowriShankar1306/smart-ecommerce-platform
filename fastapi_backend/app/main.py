import os

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.models.user import User
from app.models.category import Category
from app.models.product import Product
from app.models.cart import Cart
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.payment import Payment
from app.models.notification import Notification


from app.routers.auth import router as auth_router
from app.routers.category import router as category_router
from app.routers.product import router as product_router
from app.routers.cart import router as cart_router
from app.routers.order import router as order_router
from app.routers.payment import router as payment_router
from app.routers.notification import router as notification_router
from app.routers.websocket import router as websocket_router
from app.routers.auth0 import router as auth0_router

app = FastAPI(
    title="Smart E-Commerce API",
    description="User Panel API for Smart E-Commerce Platform",
    version="1.0.0"
)
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("JWT_SECRET_KEY")
)

app.include_router(auth_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(notification_router)
app.include_router(websocket_router)
app.include_router(auth0_router)

@app.get("/")
def root():
    return {"message": "Smart E-Commerce API is running"}

