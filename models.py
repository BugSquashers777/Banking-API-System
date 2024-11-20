# models.py
from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort
import os

db = SQLAlchemy()


class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    balance = db.Column(db.Float, default=0.0)

    # Use a unique name for the backref to avoid conflicts
    transactions = db.relationship(
        'Transaction', 
        backref='account_ref',  # Unique backref name for the reverse relationship
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Account {self.name}, {self.email}, Balance: {self.balance}>"

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    action = db.Column(db.String(10), nullable=False)

    # This creates the reverse relationship from Transaction to Account
    account = db.relationship('Account', backref='transaction_ref')  # Unique backref here as well

    def __repr__(self):
        return f"<Transaction {self.action} {self.amount} for Account {self.account_id}>"

def create_db_if_not_exists(app):
    # Check if the database file exists (assuming SQLite in this case)
    if not os.path.exists('accounts.db'):
        print("Database does not exist. Creating a new one...")
        db.create_all(app=app)


# Helper Functions

def get_account_or_404(account_id):
    account = Account.query.get(account_id)
    if not account:
        abort(404, message="Account not found")
    return account

def validate_transaction_action(action, amount, balance):
    if action not in ['deposit', 'withdraw']:
        abort(400, message="Invalid transaction action. Use 'deposit' or 'withdraw'.")
    if action == 'withdraw' and amount > balance:
        abort(406, message="Insufficient funds")
    if amount <= 0:
        abort(400, message="Amount must be greater than zero")
    return True

def validate_email(data):
    if Account.query.filter_by(email=data['email']).first():
        return False
    return True

