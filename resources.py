from flask import Flask, request
from extensions import db
from flask_restful import Resource

class DepositAddress(Resource):
    def post(self):
        addresses = request.json['addresses']


        print(request.json)