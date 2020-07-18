from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '1881d1e76e6c877770b04752b88badf4'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///resBot.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
base_url = '/v1'
from resBot import routes
from resBot import memberRoutes
from resBot import contributionRoutes
from resBot import reportRoutes