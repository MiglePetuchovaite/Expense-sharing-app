from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, FloatField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from wtforms_sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField
import app

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
    group_id = StringField('Group ID:', validators=[DataRequired()])
    submit = SubmitField('Add')

class BillForm(FlaskForm):
    amount = FloatField('Amount:', [DataRequired()])
    description = StringField('Description', [DataRequired()])
    submit = SubmitField('Add')