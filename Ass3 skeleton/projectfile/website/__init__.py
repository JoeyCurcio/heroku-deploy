#This will import everything
from flask import Flask 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

db = SQLAlchemy()


#create a function that creates a web application bootstrap = Bootstrap5(app)
# a web server will run this web application
def create_app():
  
    app = Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug = True
    app.secret_key = 'utroutoru'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    #initialize db with flask app
    db.init_app(app)

    #initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)
    
    #This will create the database
    from . import models
    with app.app_context():
      if not path.exists('website/' +' project.db'):
         db.create_all()
         print('db was created')

    #This then returns the application that was just created
    return app





