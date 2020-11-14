from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired
from devops.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('Reporter'),('Triager'),('Developer'),('Reviewer')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
       user = User.query.filter_by(username=username.data).first()
       if user:
          raise ValidationError('Username already exists.')

    def validate_email(self, email):
       user = User.query.filter_by(email=email.data).first()
       if user:
          raise ValidationError('Email already exists.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Sign in')
   
class BugForm(FlaskForm):
   summary = StringField('Summary', validators=[DataRequired()])
   product = StringField('Product', validators=[DataRequired()])
   platform = StringField('Platform', validators=[DataRequired()])
   whatHappen = TextAreaField('What Happened?', validators=[DataRequired()])
   howHappen = TextAreaField('How did it happen?', validators=[DataRequired()])
   shouldHappen = TextAreaField('What should have happened?', validators=[DataRequired()])
   status = SelectField(u'Status', choices=[('Unassigned'),('Work in progress'),('Pending for review'),('Done')], default='Unassigned')
   priority = SelectField(u'Priority', choices=[('Low'), ('High')], default='Low')
   submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
   summary = StringField('Summary', validators=[DataRequired()])
   product = StringField('Product', validators=[DataRequired()])
   platform = StringField('Platform', validators=[DataRequired()])
   whatHappen = TextAreaField('What Happened?', validators=[DataRequired()])
   howHappen = TextAreaField('How did it happen?', validators=[DataRequired()])
   shouldHappen = TextAreaField('What should have happened?', validators=[DataRequired()])
   status = SelectField(u'Status', choices=[('Unassigned'),('Work in progress'),('Pending for review'),('Done')], default='Unassigned')
   priority = SelectField(u'Priority', choices=[('Low'), ('High')], default='Low')
   assigned_to = SelectField('Assigned to', coerce=int, validators=[InputRequired()])
   reviewed_by = SelectField('Reviewed by', coerce=int, validators=[InputRequired()])
   submit = SubmitField('Submit')

class CommentForm(FlaskForm):
   comment = TextAreaField('Comment', validators=[DataRequired()])
   submit = SubmitField('Comment')