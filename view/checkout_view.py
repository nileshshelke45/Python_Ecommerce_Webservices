from flask_restx import Namespace, Resource
from service import checkout_cart

api = Namespace("checkout", description="Checkout Operation")


@api.route("/<int:user_id>")
class Checkout(Resource):
    @api.doc(
        responses={
            200: "success",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        description="This API will tell whether user can checkout or not",
        params={"user_id": "ID of a user"},
    )
    def get(self, user_id):
        """Checkout the cart"""
        res, status = checkout_cart(user_id)
        if status:
            return (res, 200)
        else:
            return (
                {"message": "Server Error Please try agin later", "error": res},
                500,
            )
