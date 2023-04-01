
class Config:
    # configure the SQLite database, relative to the app instance folder
    SECRET_KEY = '5791628bb0b13ce0c676dfde280ba245'
    SQLALCHEMY_DATABASE_URI= "sqlite:///project.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT= 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'uttampipaliya4@gmail.com'
    MAIL_PASSWORD = 'ohcdwisphksqowey'