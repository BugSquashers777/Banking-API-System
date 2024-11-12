from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

# API ENDPOINTS

class Accounts(Resource):
    #GET /accounts/<account_id>: Retrieves information about a specific account.
    def get(self, account_id):
        pass

    # POST /accounts: Creates a new account.
    def post(self, account_id = None):
        pass

    # PUT /accounts/<account_id>: Updates account information.
    def put(self, account_id):
        pass

    # DELETE /accounts/<account_id>: Deletes an account.
    def delete(self, account_id):
        pass

class Transactions(Resource):

    # POST /transactions/deposit: Adds funds to an account. or /transactions/withdraw: Withdraws funds from an account.
    def post(self, action):
        pass


api.add_resource(Accounts, "/accounts", "/accounts/<int:account_id>")
api.add_resource(Transactions, "/transactions/<string:action>")

if __name__ == "__main__":
    app.run(debug=True)