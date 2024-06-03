from models import db, User
from sqlalchemy.exc import SQLAlchemyError
from models import History, HistoryDetails
from sqlalchemy import desc
from datetime import datetime

"""this method return the list of all users"""


def get_users():
    try:
        users = User.query.all()
        return (users, True)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return (error, False)


"""this method returns the total number of users"""


def count_of_user():
    try:
        count = User.query.count()
        return (count, True)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        return (error, False)


"""this method add new user to database"""


def add_user(user):
    res, status = count_of_user()
    if status:
        try:
            new_user = User(
                user_id=res + 1,
                user_name=user.username,
                user_password=user.password,
                user_email=user.email,
            )
            db.session.add(new_user)
            db.session.commit()
            return ("User Added Successfully", True)
        except SQLAlchemyError as e:
            error = str(e.__dict__["orig"])
            return (error, False)
    else:
        return (res, False)


"""This method return the purchase history for particular user"""


def purchase_history_of_user(user_id):
    try:
        product_histories = (
            History.query.filter_by(user_id=user_id)
            .order_by(desc(History.history_id))
            .limit(5)
            .all()
        )
        if product_histories:
            new = []
            for product_history in product_histories:
                purchase_history_id = product_history.history_id
                purchase_history_details = HistoryDetails.query.filter_by(
                    history_id=purchase_history_id
                )
                lis = {}
                for purchase_history_detail in purchase_history_details:
                    lis[purchase_history_detail.product_name] = {
                        "product_id": purchase_history_detail.product_id,
                        "product_quantity": purchase_history_detail.product_quantity,
                        "product_price": purchase_history_detail.product_price,
                        "product_total_price": purchase_history_detail.product_total_price,
                    }
                new_lis = {
                    "History_Date": datetime.strftime(
                        product_history.order_created, "%Y-%m-%d"
                    ),
                    "Orders": lis,
                    "Total Price": product_history.total_price,
                }
                new.append(new_lis)
            return ({"User Purchase History": new}, True)
        else:
            return ({"message": "User does not have any purchase"}, True)
    except SQLAlchemyError as e:
        error = e.__dict__["orig"]
        return (error, False)
