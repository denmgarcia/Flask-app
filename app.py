from flask import Flask, render_template, session, redirect, url_for
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
# from flask.ext.moment import Moment
from flask_moment import Moment
from datetime import datetime
import os
# from flask.ext.wtf import Form
from flask_wtf import Form
from wtforms.fields import TextField, SubmitField, RadioField
from wtforms.validators import Required
app = Flask(__name__)
app.config['SECRET_KEY'] = "13sdf656sdf++sdfsdfdg23r6"

basedir = os.path.abspath(os.path.dirname(__file__))

bootstrap = Bootstrap(app)
moment = Moment(app)
app.config['POSTGRES_DATABASE_URI'] ='sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)


class NameForm(Form):
    name = TextField('What is your name?', validators=[Required()])
    submit = SubmitField('Submit')
    submit2 = RadioField('Label', choices=[('value','description'), 
                                           ('value_two', 'whatever')])

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)

    def __repr__(self):
        return '<Role %r>' % self.name

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.username

# @app.route('/')
# def index():
#     return '<h1>Hello World!</h1>'
@app.route('/', methods=['POST','GET'])
def index():
    form = NameForm()
    return render_template('index.html', current_time=datetime.utcnow(),form=form)

@app.route('/sema', methods=['GET', 'POST'])
def index2():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index2'))
    return render_template('index2.html',form = form, name = session.get('name'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=True)