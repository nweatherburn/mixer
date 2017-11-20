from flask import Flask

from extensions import base, db, scheduler
from settings import FlaskConfig


def create_app(config_object=FlaskConfig):
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


def initialize_db():
    base.metadata.drop_all(bind=db.engine)
    base.metadata.create_all(bind=db.engine)


app = create_app(FlaskConfig)
