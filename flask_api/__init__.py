from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://lucca10:goku4040@localhost/holiday_db'
app.config['JSON_SORT_KEYS'] = False
db=SQLAlchemy(app)

from flask_api.product.views import catalog
app.register_blueprint(catalog)
