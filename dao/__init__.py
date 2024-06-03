from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_dao import get_users, count_of_user, add_user, purchase_history_of_user
from .cart_dao import get_cart, addtocart, removefromcart, updatecart, check_user
from .product_dao import add_product
