from flask_restx import Resource, Namespace, fields, reqparse, marshal
from dao import get_users, add_user, purchase_history_of_user, check_user

api = Namespace("users", description="User Operations")

user = api.model(
    "User",
    {
        "user_id": fields.Integer(description="The unique identifier of the user"),
        "user_name": fields.String(description="The name of the user"),
        "user_password": fields.String(description="The email address of the user"),
        "user_email": fields.String(description="The password of the user"),
    },
)


@api.route("/")
class UserList(Resource):
    @api.doc(
        responses={
            200: "success",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        description="This API will return the list of users",
    )
    def get(self):
        """List of users"""
        res, status = get_users()
        if status:
            if len(res) == 0:
                return ({"message": "No user in the database"}, 200)
            else:
                return marshal(res, user), 200
        else:
            return (
                {"message": "Server Error please try again later", "error": res},
                500,
            )


@api.route("/add")
class AddUser(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username", required=True)
    parser.add_argument("password", required=True)
    parser.add_argument("email", required=True)

    @api.doc(
        responses={
            200: "success",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        description="This API will add new user",
    )
    @api.expect(parser)
    def post(self):
        """Add new user"""
        args = self.parser.parse_args()
        res, status = add_user(args)
        if status:
            return ({"messasge": res}, 201)
        else:
            return (
                {"message": "Server Error please try again later", "error": res},
                500,
            )


@api.route("/purchase_history/<int:user_id>")
class PurchaseHistory(Resource):
    @api.doc(
        responses={
            200: "success",
            201: "Created",
            204: "No Content",
            400: "Bad Request",
            404: "Not Found",
            500: "Internal Server Error",
        },
        description="This API will show last 5 purchase history detail for user",
        params={"user_id": "ID of a user"},
    )
    def get(self, user_id):
        res, status = check_user(user_id)
        if status:
            if res == "no":
                return ({"message": "User does not exist"}, 200)
        else:
            return (
                {"message": "Server Error please try again later", "error": res},
                500,
            )
        res, status = purchase_history_of_user(user_id)
        if status:
            return (res, 200)
        else:
            return (
                {"message": "Server Error please try again later", "error": res},
                500,
            )
