from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from stockapp.config import Config


# replace DATABASE_URI with the path to your SQLite database file
DATABASE_URI = 'sqlite:///project.db'

bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

mail = Mail()
db = SQLAlchemy()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # initialize the app with the extension
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from stockapp.users.routes import users
        from stockapp.main.routes import main
        from stockapp.errors.handlers import errors
        from stockapp.charts import charts
        app.register_blueprint(users)
        app.register_blueprint(main)
        app.register_blueprint(errors)
        app.register_blueprint(charts)
        db.create_all()
        return app
