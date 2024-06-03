from models import Product, db
from sqlalchemy.exc import SQLAlchemyError


"""this method will return count of products in database"""


def count_of_product():
    try:
        count = Product.query.count()
        return (count, True)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return (error, False)


"""this method will add new product in database"""


def add_product(product):
    res, status = count_of_product()
    if status:
        try:
            new_product = Product(
                product_id="PD" + str(res + 1),
                product_name=product.product_name,
                product_image=bytes(product.product_image, encoding="utf-8"),
                product_price=product.product_price,
                product_quantity=product.product_quantity,
                product_tax=product.product_tax,
            )
            db.session.add(new_product)
            db.session.commit()
            return ("Product Added Successfully", True)
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return (error, False)
    else:
        return (res, False)
