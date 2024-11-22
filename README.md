# Bank Account API

A simple Flask-based RESTful API for managing bank accounts, users, and transactions. This application allows you to create accounts, perform transactions (deposit/withdraw), and manage user accounts with authentication (login and registration).

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setup and Configuration](#setup-and-configuration)
- [API Endpoints](#api-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Account Endpoints](#account-endpoints)
  - [Transaction Endpoints](#transaction-endpoints)
- [Models](#models)
- [Database Setup](#database-setup)
- [Helper Functions](#helper-functions)
- [Error Handling](#error-handling)

## Features

- User Registration and Login with password hashing.
- Account management (create, update, delete).
- Transactions (Deposit and Withdrawal).
- Get transaction history for an account.
- Built-in validation and error handling.

## Installation

To run the Bank Account API locally, follow the steps below:

1. **Clone the repository**:

```bash
git clone https://github.com/BugSquashers777/Banking-API-System.git
cd Banking-API-System
```

2. **Install required dependencies**:
```bash
pip install -r requirements.txt
```
3. **Start the Flask application:**
On linux/Macos
```bash
python3 app.py
```
or
```commandline
python app.py
```

The application will run on http://127.0.0.1:5000.

# Setup and Configuration

## Configuring the Database

The application uses SQLite as the database. By default, the database file (accounts.db) is stored in the root directory of the project. The create_db_if_not_exists function will automatically create the database file and tables if they do not exist.

To configure or change the database settings, you can modify the SQLALCHEMY_DATABASE_URI in the app.py file.

```commandline
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
```

CORS Configuration

The API is configured to allow CORS from http://127.0.0.1:5500. This can be updated in the app.py to match your frontend URL if necessary.

# API Endpoints
## Authentication Endpoints
Get /login

    Logs in a user with username and password.
    Returns a success message and the user's email if successful, or an error message if invalid credentials.

POST /register

    Registers a new user with username, email, and password.
    Returns a success message and the created account details if successful.

PUT /login/{email}

    Allows users to update their login credentials (username/email).

Here is the content for the README in markdown format (README.md):

# Bank Account API

A simple Flask-based RESTful API for managing bank accounts, users, and transactions. This application allows you to create accounts, perform transactions (deposit/withdraw), and manage user accounts with authentication (login and registration).

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Setup and Configuration](#setup-and-configuration)
- [API Endpoints](#api-endpoints)
  - [Authentication Endpoints](#authentication-endpoints)
  - [Account Endpoints](#account-endpoints)
  - [Transaction Endpoints](#transaction-endpoints)
- [Models](#models)
- [Database Setup](#database-setup)
- [Helper Functions](#helper-functions)
- [Error Handling](#error-handling)

## Features

- User Registration and Login with password hashing.
- Account management (create, update, delete).
- Transactions (Deposit and Withdrawal).
- Get transaction history for an account.
- Built-in validation and error handling.

## Installation

To run the Bank Account API locally, follow the steps below:

1. **Clone the repository**:

```bash
git clone https://github.com/your-username/bank-account-api.git
cd bank-account-api
```
Create a virtual environment:

    python3 -m venv venv

Activate the virtual environment:

On macOS/Linux:

    source venv/bin/activate

On Windows:

    .\venv\Scripts\activate

Install required dependencies:

    pip install -r requirements.txt

Start the Flask application:

    python app.py

The application will run on http://127.0.0.1:5000.

# Setup and Configuration
## Configuring the Database

The application uses SQLite as the database. By default, the database file (accounts.db) is stored in the root directory of the project. The create_db_if_not_exists function will automatically create the database file and tables if they do not exist.

To configure or change the database settings, you can modify the SQLALCHEMY_DATABASE_URI in the app.py file.

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'

CORS Configuration

The API is configured to allow CORS from http://127.0.0.1:5500. This can be updated in the app.py to match your frontend URL if necessary.

    CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5500"}})

# API Endpoints
## Authentication Endpoints

### GET /login

- Logs in a user with username and password.
- Returns a success message and the user's email if successful, or an error message if invalid credentials.

### POST /register

- Registers a new user with username, email, and password.
- Returns a success message and the created account details if successful.

### PUT /login/{email}

- Allows users to update their login credentials (username/email).

## Account Endpoints
### POST /accounts

- Creates a new account associated with the logged-in user.
- Requires name, email, account_type, and optionally balance (defaults to 0.0).
- Returns the newly created account details if successful.

### GET /accounts/{email}

- Retrieves the account information associated with the provided email.
- Returns account details or an error message if the account is not found.

### PUT /accounts/{email}

- Updates account details for the provided email.
- Supports updating the name and email.

### DELETE /accounts/{email}

- Deletes the account associated with the provided email.

## Transaction Endpoints

### POST /transactions/{action}
- Performs a transaction (either deposit or withdraw) on an account.
- Requires account_id, amount, email, and date.
- Returns success or failure message based on the action.

### GET /transactions/history/{email}

- Retrieves the transaction history for the provided account email.
- Returns a list of transactions associated with the account.

# Models
## User Model

The User model represents a user who has login credentials and may have one or more associated accounts.

### Fields:
- user_id: Integer (Primary Key)
- username: String (Unique)
- email: String (Unique)
- password: String (Hashed password)

### Relationships:

- Each User can have multiple Account instances.

## Account Model

The Account model represents a bank account associated with a user.

### Fields:
- account_id: Integer (Primary Key)
- user_id: Integer (Foreign Key to User)
- name: String
- email: String (Unique)
- account_type: String (Default: "Savings")
- balance: Float (Default: 0.0)

### Relationships:
- Each Account belongs to one User and can have multiple Transaction instances.

## Transaction Model

The Transaction model represents a financial transaction (deposit or withdrawal) on an account.

### Fields:

- transaction_id: Integer (Primary Key)
- account_id: Integer (Foreign Key to Account)
- amount: Float
- action: String (Either "deposit" or "withdraw")
- date: String (Default: current date and time)

# Database Setup

The database file is created automatically when the application starts if it does not already exist, using the create_db_if_not_exists function. The following tables are created:

1. User: Stores information about users (username, email, password).
2. Account: Stores information about user accounts (name, email, balance).
3. Transaction: Stores transaction records for deposits and withdrawals.

# Helper Functions

## create_db_if_not_exists(app)

- Creates the database tables if they do not exist. It checks if the accounts.db file exists and creates it if necessary.

## get_account_or_404(email)

- Retrieves an account by email. If the account does not exist, it raises a 404 error.

## validate_transaction_action(action, amount, balance)

- Validates if a transaction action (deposit/withdraw) is valid. Ensures the amount is greater than zero, the transaction type is correct, and that there are sufficient funds for withdrawals.

## validate_email(data)

- Checks if an email is already in use by another account. Returns False if the email exists, otherwise returns True.

# Error Handling

The application uses Flask's built-in abort() function to handle errors and raise appropriate HTTP status codes:

    400: Bad Request (e.g., invalid data in the request).
    404: Not Found (e.g., account or user not found).
    406: Not Acceptable (e.g., insufficient funds for withdrawal).
    500: Internal Server Error (e.g., database errors or unhandled exceptions).