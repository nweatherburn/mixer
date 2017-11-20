from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
from sqlalchemy.ext.declarative import declarative_base


base = declarative_base()
db = SQLAlchemy()
scheduler = APScheduler()