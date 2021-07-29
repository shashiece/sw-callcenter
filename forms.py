from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import sqlite3

import json

with open('config/config.json') as f:
     ccConfig = json.load(f)
    
class LoginForm(FlaskForm):
 email = StringField('Email',validators=[DataRequired(),Email()])
 password = PasswordField('Password',validators=[DataRequired()])
 remember = BooleanField('Remember Me')
 submit = SubmitField('Login')
 def validate_email(self, email):
    conn = sqlite3.connect(ccConfig['settings']['database_file'])
    curs = conn.cursor()
    curs.execute("SELECT email FROM agent where email = (?)",[email.data])
    valemail = curs.fetchone()
    if valemail is None:
      raise ValidationError('This Email ID is not registered. Please register before login')
