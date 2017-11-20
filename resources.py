from flask import Flask, request
from extensions import db
from flask_restful import reqparse, Resource
from mixer import create_new_deposit_address_for_addresses 

parser = reqparse.RequestParser()

class DepositAddress(Resource):

    # def __init__(self):
    #     self.parser = reqparse.RequestParser()
    #     self.parser.add_argument('')

    def post(self):
        addresses = [a['address'] for a in request.get_json()]
        
        try:
            deposit_address = create_new_deposit_address_for_addresses(addresses)
            return {'deposit_address' : deposit_address}
        except ValueError:
            error = {
                'error' : 'One or more payment address already registered to deposit address'
            }
            return (error, 422)