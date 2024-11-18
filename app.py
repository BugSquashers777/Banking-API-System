from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'  # SQLite database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

#-----------------------------------------DATABASE----------------------------------#

# Define Account Model
class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Account {self.name}, {self.email}, Balance: {self.balance}>"

# Define Transaction Model
class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    action = db.Column(db.String(10), nullable=False)

    account = db.relationship('Account', backref='transactions')

    def __repr__(self):
        return f"<Transaction {self.action} {self.amount} for Account {self.account_id}>"

# Create tables if they don't exist
with app.app_context():
    db.create_all()


#-----------------------API ENDPOINTS---------------------------------------------------#

transactions_args = reqparse.RequestParser()
transactions_args.add_argument("account_id", type=int, help="Account ID is required.", required=True)
transactions_args.add_argument("amount", type=float, help="Amount is required.", required=True)

# Helper Functions

def get_account_or_404(account_id):
    """
    Helper function to retrieve an account or abort with 404 if not found.
    """
    account = Account.query.get(account_id)
    if not account:
        abort(404, message="Account not found")
    return account

def validate_transaction_action(action, amount, balance):
    """
    Helper function to validate the transaction action.
    """
    if action not in ['deposit', 'withdraw']:
        abort(400, message="Invalid transaction action. Use 'deposit' or 'withdraw'.")
    if action == 'withdraw' and amount > balance:
        abort(406, message="Insufficient funds")
    if amount <= 0:
        abort(400, message="Amount must be greater than zero")

class Accounts(Resource):
    """
    A class that handles operations related to user accounts.

    Methods:
        get(account_id): Retrieves information about a specific account.
        post(account_id): Creates a new account.
        put(account_id): Updates the information of a specific account.
        delete(account_id): Deletes a specific account.
    """

    def get(self, account_id):
        """
        Retrieves information about a specific account.

        Args:
            account_id (str): The unique identifier for the account.

        Returns:
            dict: Account information, such as account details and balance.
        """
        pass

    def post(self, account_id=None):
        """
        Creates a new account or updates an existing one if an account_id is provided.

        Args:
            account_id (str, optional): The unique identifier for an existing account. Default is None for creating a new account.

        Returns:
            dict: Information about the newly created or updated account.
        """
        pass

    def put(self, account_id):
        """
        Updates the information of a specific account.

        Args:
            account_id (str): The unique identifier for the account to be updated.

        Returns:
            dict: Information about the updated account.
        """
        pass

    def delete(self, account_id):
        """
        Deletes a specific account.

        Args:
            account_id (str): The unique identifier for the account to be deleted.

        Returns:
            dict: Confirmation message or status about the deletion.
        """
        pass


class Transactions(Resource):
    """
    A resource for handling financial transactions, such as deposits and withdrawals, for accounts.

    Methods:
        post(action: str): Processes a deposit or withdrawal transaction for an account based on the action.
                           Returns a success message with the updated balance and account ID.
    """
    def post(self, action):
        """
        Processes a deposit or withdrawal transaction for an account.
        """
        args = transactions_args.parse_args()
        account_id = args["account_id"]
        amount = args["amount"]

        # Fetch the account and validate the transaction
        account = get_account_or_404(account_id)
        validate_transaction_action(action, amount, account.balance)

        # Create a new transaction
        transaction = Transaction(account_id=account_id, amount=amount, action=action)
        db.session.add(transaction)

        # Update account balance
        if action == 'deposit':
            account.balance += amount
        elif action == 'withdraw':
            account.balance -= amount

        db.session.commit()

        return jsonify({
            "message": f"{action.capitalize()} successful",
            "account_id": account.account_id,
            "balance": account.balance
        })

api.add_resource(Accounts, "/accounts", "/accounts/<int:account_id>")
api.add_resource(Transactions, "/transactions/<string:action>")

if __name__ == "__main__":
    app.run(debug=True)
