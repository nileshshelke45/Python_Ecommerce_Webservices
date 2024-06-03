from . import db


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_name = db.Column(db.String(40), nullable=False)
    user_password = db.Column(db.String(128), nullable=False)
    user_email = db.Column(db.String(64), nullable=False)
    shop_cart = db.relationship("Cart", backref="users", lazy=True)
    product_history = db.relationship("History", backref="users", lazy=True)

    def __repr__(self):
        return {
            "user_id": self.user_id,
            "user_name": self.user_name,
            "user_email": self.user_email,
            "user_password": self.user_password,
        }
