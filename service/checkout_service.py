from . import Cart, CartDetails, db, HistoryDetails, History, Product
from sqlalchemy.exc import SQLAlchemyError
from service import check_cart


"""This method will change the status of cart"""


def update_checkout(cart):
    try:
        cart.checkout_status = "ok"
        db.session.commit()
        return ("ok", True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)


"""This method will fill the fields for purchase history table"""


def purchase_history(status, cart):
    try:
        count = History.query.count()
        cart = Cart.query.filter_by(
            cart_user_id=cart.cart_user_id, checkout_status=status
        ).first()
        history_id = count + 1
        if cart:
            data_purchase_history = History(
                history_id=history_id,
                user_id=cart.cart_user_id,
                total_price=cart.cart_amount,
            )
            db.session.add(data_purchase_history)
            db.session.commit()
            res, status = purchase_history_detail(cart.cart_id, history_id)
            if status:
                return (res, True)
            else:
                return (res, False)
        else:
            return ({"message": "Cart Does not exist"}, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)


"""This method will add the fields for product history detail table"""


def purchase_history_detail(cart_id, id):
    try:
        cart_details = CartDetails.query.filter_by(cart_id=cart_id).all()
        for cart_detail in cart_details:
            detail_count = HistoryDetails.query.count()
            data_purchase_history_details = HistoryDetails(
                history_detail_id=detail_count + 1,
                product_id=cart_detail.cart_product_id,
                product_name=cart_detail.products.product_name,
                product_quantity=cart_detail.cart_quantity,
                product_price=cart_detail.products.product_price,
                product_total_price=cart_detail.cart_price,
                history_id=id,
            )
            db.session.add(data_purchase_history_details)
        db.session.commit()
        return ({"message": "Order Placed "}, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, True)


"""This method will update the inventory"""


def update_inventory(products):
    try:
        for product in products:
            product_model = Product.query.filter_by(
                product_id=product.cart_product_id
            ).first()
            product_model.product_quantity = (
                product_model.product_quantity - product.cart_quantity
            )
        db.session.commit()
        return ({"message": "Inventory updated succesfully"}, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)


"""Returns the appropriate result whether the user can checkout or not"""


def checkout_cart(user_id):
    try:
        check, status = check_cart(user_id)
        if status:
            if check is None:
                return ({"message": "No Cart for the user"}, True)
        else:
            return (check, status)
        cart = Cart.query.filter_by(cart_user_id=user_id, checkout_status="no").first()
        cart_id = cart.cart_id
        products = CartDetails.query.filter_by(cart_id=cart_id).all()
        lis = {}
        for product in products:
            prod = product.products
            if prod.product_quantity == 0:
                return (
                    {
                        "message": f"Product({prod.product_name}) is not available. Please remove the product from cart"
                    },
                    True,
                )
            if product.cart_quantity > prod.product_quantity:
                lis[
                    prod.product_name
                ] = f"This much quantity for {prod.product_name} is not present. Please Lower the quantity"
        if lis:
            return (lis, True)
        else:
            res, status = purchase_history(cart.checkout_status, cart)
            if status:
                result, status_1 = update_checkout(cart)
                if not status_1:
                    return ({"message": "server Error", "error": result}, True)
                res_1, status_1 = update_inventory(products)
                if not status_1:
                    return {"message": "Server Error", "error": res_1}
                return (res, True)
            else:
                return (res, False)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)
