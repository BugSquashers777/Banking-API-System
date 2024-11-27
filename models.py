from flask_sqlalchemy import SQLAlchemy
from flask_restful import abort
import os
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # User is now a foreign key on Account
    account = db.relationship(
        'Account', 
        backref='user_ref',  # Unique backref name for the reverse relationship
        lazy=True,
        cascade="all, delete-orphan"
    )

class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False) 
    name = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(100), default="Savings")
    balance = db.Column(db.Float, default=0.0)

    user = db.relationship('User', backref='account_ref')
    # Account is now a foreign key on Transaction
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
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'), nullable=False)  # Account is now a foreign key on Transaction
    amount = db.Column(db.Float, nullable=False)
    action = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(100), default=datetime.now)

    # This creates the reverse relationship from Transaction to Account
    account = db.relationship('Account', backref='transaction_ref', overlaps="account_ref,transactions")  # Unique backref here as well

    def __repr__(self):
        return f"<Transaction {self.action} {self.amount} for Account {self.account_id}>"

def create_db_if_not_exists(app):
    # Check if the database file exists (assuming SQLite in this case)
    if not os.path.exists('accounts.db'):
        print("Database does not exist. Creating a new one...")
        with app.app_context():
            db.create_all()


# Helper Functions

def get_account_or_404(email):
    user = User.query.filter_by(email=email).first()
    account = Account.query.filter_by(user_id=user.user_id).first()
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
    if User.query.filter_by(email=data['email']).first():
        return False
    return True

