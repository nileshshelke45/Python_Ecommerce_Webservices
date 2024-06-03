from dao import get_cart, addtocart, removefromcart, updatecart
from flask_restx import Resource, Namespace, fields, reqparse, marshal

api = Namespace("cart", description="Cart Operations")


cart = api.model(
    "Cart",
    {
        "cart_id": fields.String(description="The unique identifier of the cart"),
        "cart_user_id": fields.Integer(description="The id of the user"),
        "cart_amount": fields.Float(description="The total amount of cart"),
        "create_date": fields.Date(description="Day cart is created"),
        "checkout_status": fields.String(description="checkout_status"),
    },
)


@api.route("/view/<int:user_id>")
class CartList(Resource):
    @api.doc(
        responses={
            200: "success",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        description="This API will return the cart associated  with particular users",
        params={"user_id": "ID of a user"},
    )
    def get(self, user_id):
        """Get a cart for a particular user"""
        res, status = get_cart(user_id)
        if status:
            if res == "None":
                return ({"message": "No Cart for the user"}, 200)

            elif res == "no":
                return ({"message": "Sorry, User with this id does not exist"}, 200)

            return res, 200
        else:
            return (
                {"message": "Server Error please try again later", "error": res},
                500,
            )


@api.route("/add/<int:user_id>")
class AddtoCart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("product_id", type=str, required=True)
    parser.add_argument("quantity", type=int, required=True)

    # parser.add_argument('price', type=float,required=True)
    @api.doc(
        responses={
            200: "success",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        description="This API will the add product to cart associated  with particular users",
        params={"user_id": "ID of a user"},
    )
    @api.expect(parser)
    def post(self, user_id):
        """Add new product to cart for a particular user"""
        args = self.parser.parse_args()
        res, status = addtocart(args, user_id)
        if status:
            if res == "no":
                return ({"message": "User does not exist for this id"}, 200)
            else:
                return (res, 200)

        else:
            return (
                {"message": "Server Error please try again later", "error": res},
                500,
            )


@api.route("/remove/<int:user_id>")
class RemovetoCart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("product_id", type=str, required=True)

    @api.doc(
        responses={
            200: "success",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        description="This API will remove the product from cart associated with particular users",
        params={"user_id": "ID of a user"},
    )
    @api.expect(parser)
    def delete(self, user_id):
        """Remove Product from a cart for a particular user"""
        args = self.parser.parse_args()
        res, status = removefromcart(user_id, args)
        if status:
            if res == "no":
                return ({"message": "User for this ID does not exist"}, 200)
            else:
                return (res, 200)
        else:
            return ({"message": "Server error", "error": res}, 500)


@api.route("/update/<int:user_id>")
class UpdateCart(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("product_id", type=str, required=True)
    parser.add_argument("quantity", type=int, required=True)

    @api.doc(
        responses={
            200: "success",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        description="This API will update the particular product for a associated user",
        params={"user_id": "ID of a user"},
    )
    @api.expect(parser)
    def put(self, user_id):
        """Update product in a cart for a particular user"""
        args = self.parser.parse_args()
        res, status = updatecart(user_id, args)
        if status:
            if res == "no":
                return ({"message": "User for this ID does not exist"}, 200)
            else:
                return (res, 200)
        else:
            return ({"message": "Some Server Error", "error": res}, 500)
