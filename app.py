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
        result = Account.query.filter_by(account_id=account_id).first()
        if not result:
            abort(404, message="Could not find account with that id")
        return result

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
    A class that handles transactions related to user accounts, such as deposits and withdrawals.

    Methods:
        post(action): Performs a transaction such as deposit or withdrawal.
    """

    def post(self, action):
        """
        Processes a deposit or withdrawal transaction for an account.

        Args:
            action (str): The type of transaction, either 'deposit' or 'withdraw'.

        Returns:
            dict: The result of the transaction, including updated account balance or an error message.
        """
        pass


api.add_resource(Accounts, "/accounts", "/accounts/<int:account_id>")
api.add_resource(Transactions, "/transactions/<string:action>")

if __name__ == "__main__":
    app.run(debug=True)
