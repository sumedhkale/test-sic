"""Initialize Flask app."""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os


def invalid_api_usage(e):
    return jsonify(e.to_dict()), e.status_code


class RestError(Exception):

    def __init__(self, err_message="", err_code=404, payload=None):
        super(RestError, self).__init__()
        self.status_code = err_code
        self.err_message = err_message if err_message else "No error message provided"
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        print("ERROR: " + self.err_message)
        rv['err_message'] = self.err_message
        return rv


db = SQLAlchemy()


def create_app():
    """Create Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')

    db.init_app(app)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SECRET_KEY'] = 'super secret key'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shopify.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'shopify.db')

    with app.app_context():
        # Import parts of our application
        from app.routes.inventory_routes import inventory_bp

        # Register Blueprints
        app.register_blueprint(inventory_bp)

        # create tables
        db.drop_all()
        db.create_all()

        # add error handler
        app.register_error_handler(RestError, invalid_api_usage)

        return app