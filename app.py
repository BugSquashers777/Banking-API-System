from flask import Flask, jsonify, request
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

#-----------------------HELPER FUNCTIONS------------------------------------------------#

def validate_email(data):
    """
        Helper function to retrieve an validate email abort with 404 if already exists.
    """
    if Account.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400

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
        # Query the account from database
        account = Account.query.get(account_id)
        
        # Check if account exists
        if not account:
            return {'message': 'Account not found'}, 404
            
        # Return account information
        return {
            'account_id': account.account_id,
            'name': account.name,
            'email': account.email,
            'balance': account.balance
        }, 200

    def post(self, account_id=None):
        """
        Creates a new account.

        Args:
            account_id (str, optional): Not used, kept for API consistency.

        Returns:if Account.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400
            dict: Information about the newly created account.
        """
        data = request.get_json()
        
        if not data or 'name' not in data or 'email' not in data:
            return {'message': 'Missing required fields: name and email required'}, 400
            
        # Validate initial balance if provided
        initial_balance = data.get('balance', 0.0)
        if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
            return {'message': 'Balance must be a non-negative number'}, 400
            
        # Check if email already exists
        validate_email(data)
            
        # Create new account based on Account model fields
        account = Account(
            name=data['name'],
            email=data['email'],
            balance=initial_balance
        )
        db.session.add(account)
            
        try:
            db.session.commit()
            # Return the newly created account details along with a success message and 201 Created status
            # Return 201 status code to indicate successful resource creation (new account)
            return {
                'account_id': account.account_id,
                'name': account.name,
                'email': account.email,
                'balance': account.balance,
                'message': 'Account created successfully'
            }, 201
        except Exception as e:
            db.session.rollback()
            # Return 500 Internal Server Error when database commit fails
            return {'message': 'An error occurred while saving the account'}, 500

    def put(self, account_id):
        """
        Updates the information of a specific account.

        Args:
            account_id (str): The unique identifier for the account to be updated.

        Returns:
            dict: Information about the updated account.
        """
        account = get_account_or_404(account_id)

        data = request.get_json()

        if not data:
            return jsonify({'message': 'No data provided.'}, 400)
        
        if 'name' in data:
            account.name = data['name']
        if 'email' in data:
            validate_email(data)
            account.email = data['email']
        try:
            db.session.commit()
            return {
                'account_id': account.account_id,
                'name': account.name,
                'email': account.email,
                'balance': account.balance,
                'message': 'Account updated successfully'
            }, 201
        except Exception as e:
            db.session.rollback()
            # Return 500 Internal Server Error when database commit fails
            return {'message': 'An error occurred while updating the account'}, 500


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
