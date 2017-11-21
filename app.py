from flask import Flask

from extensions import api, db, scheduler
from resources import DepositAddress
from settings import AppConfig



def create_app(config_object=AppConfig):
    app = Flask(__name__.split('.')[0])
    app.config.from_object(config_object)
    register_extensions(app)
    initialize_db()

    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)

    scheduler.init_app(app)
    scheduler.start()

    api.app = app
    api.add_resource(DepositAddress, '/mixer/address')


def initialize_db():
    # Not great for a production system
    # Good for a demo
    db.drop_all()
    db.create_all()


app = create_app(AppConfig)
