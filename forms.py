from wtforms import StringField, PasswordField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    """User register form"""
    username = StringField("Username", validators=[DataRequired(), 
                                                   Length(min=1, max=30)])
    password = PasswordField("Password", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    first_name = StringField("First Name", validators=[DataRequired(), 
                                                       Length(min=1, max=30)])
    last_name = StringField("Last Name", validators=[DataRequired(), 
                                                     Length(min=1, max=30)])

class UserLoginForm(FlaskForm):
    """Login form"""
    username = StringField("Username", validators=[DataRequired(), 
                                                   Length(min=1, max=30)])
    password = PasswordField("Password", validators=[DataRequired()])

class FeedbackForm(FlaskForm):
    """Feedback Form"""
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()])
