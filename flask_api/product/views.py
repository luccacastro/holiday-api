import json 
import os
from flask import request, jsonify, Blueprint, abort
from flask.views import MethodView
from flask_api import db, app
from flask_api.product.utils import HolidayBr
from flask_api.product.utils import Holiday
import jwt
import datetime
from functools import wraps
import uuid
# import ast

catalog = Blueprint('catalog', __name__)
holiday = Holiday()

@catalog.route('/')
@catalog.route('/home')
def home():
    return "Welcome to the Catalog Home"

class ProductView(MethodView):
    def post(self):
        data = request.get_json()
        print(data)
        # data_dict = ast.literal_eval(data.decode('utf-8'))
        initial = data['initialDate']
        end = data['endDate']
        # location = data['location']
        cep = data['endereco_cep']
        # print(initial)
        response = jsonify(holiday.findHolidaysOnDateRange(initial, end, cep))
        return response
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         if 'x-access-token' in request.headers:
#             token = request.headers=['x-access-token']
#         if not token:
#             return jsonify({'message':'Token is missing'}), 401
    

product_view = ProductView.as_view('product_view')
app.add_url_rule('/holiday/', view_func=product_view, methods=['POST'])



1 . - False _. -> T
2.- False -> 
3.- 2 -> is true -> F


48 -> jsonify
24 -> pleno
12 -> senior

840*2
420*2
210