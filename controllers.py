from models import db, Account, Transaction, User, validate_email, validate_transaction_action, get_account_or_404
from flask import jsonify


def get_account(email):
    account = get_account_or_404(email)
    if not account:
        return {'message': 'Account not found'}, 404
    return {
        'account_id': account.account_id,
        'name': account.name,
        'email': account.email,
        'balance': account.balance
    }, 200

def create_login_account(data):
    
    if not validate_email(data):
        return {'message': 'Email already exists'}, 400
    
    
    user_account = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    db.session.add(user_account)
    try:
        db.session.commit()
        return jsonify({
            'account_id': user_account.account_id,
            'username': user_account.username,
            'email': user_account.email,
            'message': 'Account created successfully'
        }, 201)
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'An error occurred while saving the account'}, 500)

def login_validation(data):
    
    if not data or 'username' not in data or 'password' not in data:
        return {'message': 'Missing required fields: username and password required'}, 400
    
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return {'message': 'Invalid username'}, 401
    
    return user.password

def get_user_id_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return user.user_id
    return None

def get_email_by_username(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return user.email
    return None

def get_account_id_by_email(email):
    account = Account.query.filter_by(email=email).first()
    if account:
        return account.account_id
    return None


def create_account(data):
    if not data or 'name' not in data or 'email' not in data:
        return {'message': 'Missing required fields: name and email required'}, 400

    initial_balance = data.get('balance', 0.0)

    if not isinstance(initial_balance, (int, float)) or initial_balance < 0:
        return {'message': 'Balance must be a non-negative number'}, 400
    
    user_id = get_user_id_by_email(data['email'])

    account = Account(
        name=data['name'],
        user_id=user_id,
        email=data['email'],
        account_type=data['account_type'],
        balance=initial_balance
    )
    
    db.session.add(account)
    try:
        db.session.commit()
        return {
            'account_id': account.account_id,
            'name': account.name,
            'email': account.email,
            'balance': account.balance,
            'account_type': account.account_type,
            'message': 'Account created successfully'
        }, 201
    except Exception:
        db.session.rollback()
        return {'message': 'An error occurred while saving the account'}, 500


def update_account(email, data):
    account = get_account_or_404(email)
    
    if 'name' in data:
        if data["name"].strip() != "":
            account.name = data['name'] 
    # if 'email' in data:
    #     if not validate_email(data) and data['email'].strip() != "":
    #         return {'message': 'Email already exists'}, 400
        
    if data['email'].strip() != "":
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
    except Exception:
        db.session.rollback()
        return {'message': 'An error occurred while updating the account'}, 500


def update_login_account(email, data):
    user = User.query.filter_by(email=email).first()
    if not user:
        return {'message': 'User not found'}, 404
    
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']

    try:
        db.session.commit()
        return {'message': 'User updated successfully'}, 201
    except Exception:
        db.session.rollback()
        return {'message': 'An error occurred while updating the user'}, 500


def delete_account(account_id):
    # Retrieve the account or raise a 404 error if not found
    account = Account.query.filter_by(account_id=account_id).first()
    
    # Attempt to delete the account
    db.session.delete(account)
    
    try:
        # Commit the changes to the database
        db.session.commit()
        return {'message': 'Account deleted successfully'}, 204
    except Exception as e:
        # Rollback the session in case of an error
        db.session.rollback()
        return {'message': f'An error occurred while deleting the account: {str(e)} {account}'}, 500



def process_transaction(action, email, amount, account_id, date):
    account = get_account_or_404(email)
    if not account:
        return {'message': 'Account not found'}, 404
    
    try:
        if not validate_transaction_action(action, amount, account.balance):
            return {'message': f'Invalid transaction action {amount}'}, 400
        
        transaction = Transaction(account_id=account_id, amount=amount, action=action, date=date)
        db.session.add(transaction)

        if action == 'deposit':
            account.balance += amount
        elif action == 'withdraw':
            account.balance -= amount

        db.session.commit()
        return jsonify([{
            "message": f"{action.capitalize()} successful",
            "account_id": account.account_id,
            "balance": account.balance
        }, 200])
    except Exception as e:
        db.session.rollback()
        return {'message': f'An error occurred while processing transaction: {str(e)}'}, 500
    
def get_transactions(email):
    account = get_account_or_404(email)
    if not account:
        return {'message': 'Account not found'}, 404
    try:
        transactions = Transaction.query.filter_by(account_id=account.account_id)\
            .order_by(Transaction.date.desc())\
            .all()
        
        # Serialize transactions
        transactions_list = [{
            'transaction_id': t.transaction_id,
            'account_id': t.account_id,
            'amount': t.amount,
            'action': t.action,
            'date': t.date
        } for t in transactions]
        
        return jsonify(transactions_list)
    except Exception as e:
        return {'message': f'Error fetching transactions: {str(e)}'}, 500


