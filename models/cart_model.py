from datetime import datetime
from sqlalchemy import ForeignKey

from . import db


class Cart(db.Model):
    __tablename__ = "cart"
    cart_id = db.Column(db.String(20), primary_key=True, nullable=False)
    cart_user_id = db.Column(db.Integer, ForeignKey("users.user_id"), nullable=False)
    cart_amount = db.Column(db.Float, nullable=False)
    create_date = db.Column(db.Date, default=datetime.utcnow().date())
    checkout_status = db.Column(db.String(10))
    cart_detail = db.relationship("CartDetails", backref="cart", lazy=True)

    def __repr__(self):
        return {
            "cart_id": self.cart_id,
            "cart_user_id": self.cart_user_id,
            "cart_amount": self.cart_amount,
            "create_date": self.create_date,
            "checkout_status": self.checkout_status,
        }


class CartDetails(db.Model):
    __tablename__ = "cart_details"
    detail_id = db.Column(db.Integer, primary_key=True, nullable=False)
    cart_id = db.Column(db.String, ForeignKey("cart.cart_id"), nullable=False)
    cart_product_id = db.Column(
        db.String, ForeignKey("products.product_id"), nullable=False
    )
    cart_price = db.Column(db.Float, nullable=False)
    cart_quantity = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return {
            "detail_id": self.detail_id,
            "cart_id": self.cart_id,
            "cart_product_id": self.cart_product_id,
            "cart_price": self.cart_price,
            "cart_quantity": self.cart_quantity,
        }
