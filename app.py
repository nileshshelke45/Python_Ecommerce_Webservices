from flask import Flask
from flask_restx import Api, Resource, Namespace
from dao import db
from view import user_api, cart_api, product_api, checkout_api

app = Flask(__name__)
api = Api(
    app,
    version="1.0",
    title="E-Commerce API",
    description="A E-Commerce Web Service API",
)
app.config.from_pyfile("config.py")

db.init_app(app)

post_api = Namespace("postman", description="Connect to postman")


@post_api.route("/")
class Postman(Resource):
    def get(self):
        """URL to connect to postman"""
        urlvars = False  # Build query strings in URLs
        swagger = False  # Export Swagger specifications
        return api.as_postman(urlvars=urlvars, swagger=swagger), 200


api.add_namespace(post_api)
api.add_namespace(user_api)
api.add_namespace(cart_api)
api.add_namespace(product_api)
api.add_namespace(checkout_api)

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run()
