from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo
import app
from app import Group

class RegisterForm(FlaskForm):
    name = StringField('Full Name', [DataRequired()])
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    repeat_password = PasswordField("Repeat Password", [EqualTo('password', "Password have to macth.")])
    submit = SubmitField('Register')

    def check_name(self, name):
        user = app.User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError('This name is used. Please enter other name.')

    def check_email(self, email):
        user = app.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is used. Please enter other email.')
            
class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class AddGroupForm(FlaskForm):
    group_id = SelectField('Group ID:', coerce=int, choices=[(group.id, group.group_id) for group in Group.query.order_by('id')])
    submit = SubmitField('Add')


class BillForm(FlaskForm):
    amount = FloatField('Amount:', [DataRequired()])
    description = StringField('Description:', [DataRequired()])
    submit = SubmitField('Add')