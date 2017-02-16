from flask import Flask, g, render_template, flash, redirect, url_for, request, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_pagedown import PageDown

import forms
import models

DEBUG = True
PORT = 8000
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'neyioyei,sfvfvnefenis,3435.eooetoe,wyiywiy!5*'
pagedown = PageDown(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before each request"""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    """" close the database connection after each request."""
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Thank you for registering. Welcome to IdeaBox", "Success")
        models.User.create_user(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('profile'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("you've been logged in. Welcome", "success")
                return redirect(url_for('profile'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/home')
@login_required
def home():
    ideas = models.Idea.select().limit(100)
    users = models.User.select().limit(100)
    return render_template('home.html', ideas=ideas, users=users)


@app.route('/profile')
@app.route('/profile/<username>')
@login_required
def profile(username=None):
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username == username).get()
        except models.DoesNotExist:
            abort(404)

        stream = user.ideas.limit(100)
    else:
        stream = current_user.get_ideas().limit(100)
    return render_template('profile.html', stream=stream)


@app.route('/new_idea', methods=('GET', 'POST'))
@login_required
def idea():
    form = forms.IdeaForm()
    if form.validate_on_submit():
        models.Idea.create(user=g.user._get_current_object(),
                           title=form.title.data.strip(),
                           description=form.description.data)
        flash("Awesome. You have posted a new idea", "Success")
        return redirect(url_for('profile'))
    return render_template('post_idea.html', form=form)


@app.route('/view_idea/<int:idea_id>', methods=('GET', 'POST'))
@login_required
def view_idea(idea_id=None):
    idea_number = request.args.get('idea_id', idea_id)
    try:
        my_idea = models.Idea.select().where(models.Idea.id == idea_number).get()
    except models.DoesNotExist:
        abort(404)

    comment = models.Comment.select().where(models.Comment.idea == idea_id)
    comment_stream = comment.limit(100)
    form = forms.CommentForm()
    if form.validate_on_submit():
        models.Comment.create(user=g.user._get_current_object(),
                              idea=my_idea,
                              comment=form.comment.data)
        flash("Awesome. You have posted a new idea", "Success")
    return render_template('view_idea.html', my_idea=my_idea, comment_stream=comment_stream, form=form)


# @app.route('/new_comment', methods=('GET', 'POST'))
# @login_required
# def comment():
#     form = forms.CommentForm()
#     if form.validate_on_submit():
#         models.Comment.create(user=g.user._get_current_object(),
#                               idea=idea._get_current_object(),
#                               comment=form.comment.data)
#         flash("Awesome. You have posted a new idea", "Success")
#         return redirect(url_for('view'))
#     return render_template('view_idea.html', form=form)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            first_name='John',
            last_name='Doe',
            username='Jd',
            email='johndoe@gmail.com',
            password='password'
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT)
