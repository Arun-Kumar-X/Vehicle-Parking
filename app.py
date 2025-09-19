from flask import Flask
from applications.database import db

def create_app():
    app = Flask(__name__)
    app.debug = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Vehicle-Parking.db"
    db.init_app(app)
    app.app_context().push()

    return app
app = create_app()

from applications.controllers import *


if __name__ == '__main__':
    app.run(debug=True)