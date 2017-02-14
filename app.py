from flask import Flask, g
from flask.ext.login import LoginManager

import models
DEBUG = True
PORT = 8000
HOST = '0.0.0.0'

app = Flask(__name__)
app.secret_key = 'neyioyei,sfvfvnefenis,3435.eooetoe,wyiywiy!5*'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user():
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExists:
        return None

@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    """" close the database connection after each request."""
    g.db.close()
    return response

if __name__ == '__main__':
    models.initialize()
    models.User.create_user(
        first_name='John',
        last_name='Doe',
        username='Jd',
        email='johndoe@gmail.com',
        password ='password'
    )
    app.run(debug=DEBUG, host=HOST, port=PORT)
