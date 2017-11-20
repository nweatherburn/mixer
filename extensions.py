from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler

api = Api()
db = SQLAlchemy()
scheduler = APScheduler()