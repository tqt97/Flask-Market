from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        if user := User.query.filter_by(username=username_to_check.data).first():
            raise ValidationError(
                'Username already exists! Please choose another one.')

    def validate_email_address(self, email_address_to_check):
        if email := User.query.filter_by(email_address=email_address_to_check.data).first():
            raise ValidationError(
                'Email address already exists! Please choose another one.')

    username = StringField('Username :', validators=[
                           Length(min=4, max=20), DataRequired()])
    email_address = StringField('Email :', validators=[
                                Email(), DataRequired()])
    password1 = PasswordField('Password :', validators=[
                              Length(min=4, max=20), DataRequired()])
    password2 = PasswordField('Password confirm :',
                              validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username :', validators=[DataRequired()])
    password = PasswordField('Password :', validators=[DataRequired()])
    submit = SubmitField('Login')


class PurchaseForm(FlaskForm):
    submit = SubmitField('Purchase item')


class SellItemForm(FlaskForm):
    submit = SubmitField('Sell item')
