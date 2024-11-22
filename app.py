from flask import Flask, jsonify, request
from flask_bcrypt import Bcrypt
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from models import db,create_db_if_not_exists
from controllers import create_account, update_account, delete_account, get_account, process_transaction, create_login_account, login_validation, get_email_by_username, get_account_id_by_email, update_login_account, get_transactions

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app, 
     resources={r"/*": {
         "origins": "http://127.0.0.1:5500",
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization"],
         "supports_credentials": True
     }}
)

bcrypt = Bcrypt(app)
db.init_app(app)
create_db_if_not_exists(app)
api = Api(app)

# Define Argument Parsers
# transactions_args = reqparse.RequestParser()
# transactions_args.add_argument("account_id", type=int, help="Account ID is required.", required=True)
# transactions_args.add_argument("amount", type=float, help="Amount is required.", required=True)
# transactions_args.add_argument("email", type=str, help="Email is required.", required=True)

class Accounts(Resource):
    def get(self, email):
        return get_account(email)  # Delegate to controller

    def post(self):
        data = request.get_json()
        return create_account(data)

    def put(self, email):
        data = request.get_json()
        return update_account(email, data)

    def delete(self, email):
        return delete_account(email)

class Transactions(Resource):
    def post(self, action):
        data = request.get_json()
        email = data["email"]
        amount = data["amount"]
        account_id = data["account_id"]
        date = data["date"]
        return process_transaction(action, email, amount, account_id, date)
    def get(self, email):
        return get_transactions(email)

class Auth(Resource):
    def put(self, email):
        data = request.get_json()
        return update_login_account(email, data)
    def post(self):
        data = request.get_json()

        if not data or 'password' not in data or 'email' not in data or 'username' not in data:
            return {'message': 'Missing required fields: username, email and password required'}, 400
        else:
            password = data['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            data['password'] = hashed_password
        return create_login_account(data)
    def get(self):
        args = request.args
        hashed_password = login_validation(args)

        email = get_email_by_username(args['username'])
        
        if bcrypt.check_password_hash(hashed_password, args['password']):
            return {
                'username': args['username'], 
                'email': email,
                'message': 'Login successful'}, 200
        else:
            return {'message': 'Invalid password'}, 401

api.add_resource(Auth, "/login", "/register", "/login/<string:email>")
api.add_resource(Accounts, "/accounts", "/accounts/<string:email>")
api.add_resource(Transactions, "/transactions/<string:action>", "/transactions/history/<string:email>")

if __name__ == "__main__":
    app.run(debug=True)