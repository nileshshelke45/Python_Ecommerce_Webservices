from . import Cart, CartDetails, Product, User, db
from sqlalchemy.exc import SQLAlchemyError

"""This method will check is user with particular id is present or not"""


def check_user(id):
    try:
        user = User.query.filter_by(user_id=id).first()
        if user:
            return ("user exist", True)
        else:
            return ("no", True)
    except Exception as e:
        error = type(e).__name__
        return (error, False)


"""This will return the number of cart rows"""


def count_cart_rows():
    try:
        count = Cart.query.count()
        return (count, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)


"""This will return number of cart_detail_rows"""


def count_cart_detail_rows():
    try:
        count = CartDetails.query.count()
        return (count, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)


"""This will check if the user has cart or not"""


def check_cart(id):
    try:
        cart = Cart.query.filter_by(cart_user_id=id, checkout_status="no").first()
        if cart:
            return (cart.cart_id, True)
        else:
            return (cart, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)


"""This will check if particular product is present or not"""


def check_product(id):
    try:
        product = Product.query.filter_by(product_id=id).first()
        if not product:
            return (None, True)
        return (product, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)


"""This method will create a cart for partricular user"""


def create_cart(id):
    try:
        count, status = count_cart_rows()
        if not status:
            return (count, False)
        new_cart_id = "CR" + str(count + 1)
        new_cart = Cart(
            cart_id=new_cart_id,
            cart_user_id=int(id),
            cart_amount=0.00,
            checkout_status="no",
        )
        db.session.add(new_cart)
        db.session.commit()
        return new_cart_id
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return (error, False)


"""This method will delete the product from cart"""


def deletefromcart(id, cart):
    try:
        cart_details = CartDetails.query.filter_by(
            cart_id=id, cart_product_id=cart.product_id
        ).first()
        if not cart_details:
            return (
                {"message": f"No Product with product id {cart.product_id} in cart"},
                True,
            )
        cart = Cart.query.filter_by(cart_id=id).first()
        cart.cart_amount = round(cart.cart_amount - cart_details.cart_price, 2)
        if cart.cart_amount == 0:
            db.session.delete(cart)
        db.session.delete(cart_details)
        db.session.commit()
        return ({"message": "Product deleted from cart"}, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)


"""This method will add product to cart for particular user"""


def addtocartdetail(cart_id, product):
    try:
        prod = Product.query.filter_by(product_id=product.product_id).first()
        product_price = prod.product_price
        cart = Cart.query.filter_by(cart_id=cart_id).first()
        cart_detail = CartDetails.query.filter_by(
            cart_id=cart_id, cart_product_id=product.product_id
        ).first()
        tax_rate = round(1 + (prod.product_tax / 100), 2)
        if cart_detail:
            cart_detail.cart_quantity = 1 + cart_detail.cart_quantity
            cart_detail.cart_price = round(
                product_price * cart_detail.cart_quantity * tax_rate, 2
            )
            cart.cart_amount = round(
                cart.cart_amount + (product_price * 1 * tax_rate), 2
            )
            db.session.commit()
            return (
                {"message": "Product Already added to Cart quantity increased by 1"},
                True,
            )
        count_details, status = count_cart_detail_rows()
        if not status:
            return (count_details, False)
        data = CartDetails(
            detail_id=count_details + 1,
            cart_id=cart_id,
            cart_product_id=product.product_id,
            cart_price=round(float(product_price * product.quantity * tax_rate), 2),
            cart_quantity=product.quantity,
        )
        new_cart_amount = round(product_price * product.quantity * tax_rate, 2)
        if cart:
            cart_amount = cart.cart_amount + new_cart_amount
        else:
            cart_amount = new_cart_amount
        cart.cart_amount = round(cart_amount, 2)
        db.session.add(data)
        db.session.commit()
        return ({"message": "Product added to cart"}, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)
