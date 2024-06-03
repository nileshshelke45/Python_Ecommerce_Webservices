from . import db


class Product(db.Model):
    __tablename__ = "products"
    product_id = db.Column(db.String(10), primary_key=True, nullable=False)
    product_name = db.Column(db.String(40), nullable=False)
    product_image = db.Column(db.LargeBinary, nullable=False)
    product_price = db.Column(db.Float, nullable=False)
    product_quantity = db.Column(db.Integer, nullable=False)
    product_tax = db.Column(db.Integer, nullable=False)
    product_detail = db.relationship("CartDetails", backref="products", lazy=True)

    def __repr__(self):
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "product_image": self.product_image,
            "product_price": self.product_price,
            "product_quantity": self.product_quantity,
            "product_tax": self.product_tax,
        }
