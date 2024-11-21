from flask import Flask, jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from models import db,create_db_if_not_exists
from controllers import create_account, update_account, delete_account, get_account, process_transaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
create_db_if_not_exists(app)
api = Api(app)
CORS(app)

# Define Argument Parsers
transactions_args = reqparse.RequestParser()
transactions_args.add_argument("account_id", type=int, help="Account ID is required.", required=True)
transactions_args.add_argument("amount", type=float, help="Amount is required.", required=True)

class Accounts(Resource):
    def get(self, account_id):
        return get_account(account_id)  # Delegate to controller

    def post(self):
        data = request.get_json()
        return create_account(data)

    def put(self, account_id):
        data = request.get_json()
        return update_account(account_id, data)

    def delete(self, account_id):
        return delete_account(account_id)

class Transactions(Resource):
    def post(self, action):
        args = transactions_args.parse_args()
        account_id = args["account_id"]
        amount = args["amount"]
        return process_transaction(action, account_id, amount)

api.add_resource(Accounts, "/accounts", "/accounts/<int:account_id>")
api.add_resource(Transactions, "/transactions/<string:action>")

if __name__ == "__main__":
    app.run(debug=True)
