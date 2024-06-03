from . import db
from sqlalchemy import ForeignKey
from datetime import datetime


class History(db.Model):
    __tablename__ = "purchase_history"
    history_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey("users.user_id"), nullable=False)
    order_created = db.Column(db.Date, default=datetime.utcnow().date(), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    history_detail = db.relationship(
        "HistoryDetails", backref="purchase_history", lazy=True
    )

    def __repr__(self):
        return {
            "history_id": self.history_id,
            "user_id": self.user_id,
            "order_created": self.order_created,
            "total_price": self.total_price,
        }


class HistoryDetails(db.Model):
    __tablename__ = "purchase_history_details"
    history_detail_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.String, nullable=False)
    product_name = db.Column(db.String, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_total_price = db.Column(db.Float, nullable=False)
    history_id = db.Column(
        db.Integer, ForeignKey("purchase_history.history_id"), nullable=False
    )
