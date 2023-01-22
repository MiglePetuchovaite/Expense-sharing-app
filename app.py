import os
from flask import Flask, render_template, redirect, flash, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy import get_debug_queries
from flask_bcrypt import Bcrypt

from flask_login import LoginManager, UserMixin, current_user, logout_user, login_user, login_required
import forms

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.app_context().push()
app.config['SECRET_KEY'] = '4654f5dfadsrfasdr54e6rae'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'bills.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'register'
login_manager.login_message_category = 'info'

groups_users = db.Table('groups_users', db.metadata,
    db.Column('id', db.Integer, primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('groups.id')),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')))

class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column("Full Name", db.String(20), unique=True, nullable=False)
    email = db.Column("Email", db.String(120), unique=True, nullable=False)
    password = db.Column("Password", db.String(60), unique=True, nullable=False)
    groups = db.relationship('Group', secondary=groups_users)


class Group(db.Model):
    __tablename__ = "groups"
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column("Group ID", db.String(20), nullable=False)
    name = db.Column("Name", db.String(20), nullable=False)
    users = db.relationship('User', secondary=groups_users)

    def __init__(self, group_id, name ):
        self.group_id = group_id
        self.name = name

    def __repr__(self):
        return f'{self.group_id} - {self.name}'

class Bill(db.Model):
    __tablename__ = "bill"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column("Amount", db.Integer)
    description = db.Column("Description", db.String(220), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    db.create_all()
    return User.query.get(int(user_id))


@app.route("/register", methods=['GET', 'POST'])
def register():
    db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        coded_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=coded_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration Successful! Login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Failed to sign in. Check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/groups', methods=['GET', 'POST'])
@login_required
def add_group():
    data = current_user.groups
    forma = forms.AddGroupForm()
    if forma.validate_on_submit():
        group = Group.query.get(forma.group_id.data)
        if group is None:
            return render_template('groups.html', form=forma, data=data)
        group.users.append(current_user)
        db.session.add(group)
        db.session.commit()
        data = current_user.groups
        return render_template('groups.html', form=forma, data=data)
    return render_template('groups.html', form=forma, data=data)


@app.route('/bills', methods=['GET', 'POST'])
@login_required
def bills():
    db.create_all()
    data = Bill.query.all()
    forma = forms.BillForm()
    if forma.validate_on_submit():
        new_bill = Bill(amount=forma.amount.data, description=forma.description.data)
        db.session.add(new_bill)
        db.session.commit()
        data = Bill.query.all()
        flash(f"Bill is added", 'success')
        return redirect(url_for('bills'))
    return render_template('bills.html', form=forma, data=data)


@app.route('/')
def index():
  return render_template('index.html')


if __name__ == '__main__':
    db.create_all()
    app.run(host='127.0.0.1', port=8000, debug=True)
    
  