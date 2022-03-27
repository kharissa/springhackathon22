from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from bahay.models import User

class RegistrationForm(FlaskForm):
    """ Register new user form. """
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_email(self, email):
        """ Raise error if non-unique email. """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please log in.')

class LoginForm(FlaskForm):
    """ Login a registered user form. """
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")

class CreateForm(FlaskForm):
    """ Create a new home form. """
    name = StringField("House Name", validators=[DataRequired()])
    code = StringField("Join Code", validators=[DataRequired()])
    submit = SubmitField("Create House")

class JoinForm(FlaskForm):
    """ Join a household. """
    code = StringField("Join Code", validators=[DataRequired()])
    submit = SubmitField("Join House")

class AddRoomForm(FlaskForm):
    """ Add a new room to a house. """
    name = StringField("Room Name", validators=[DataRequired()], render_kw={"placeholder": "Living Room"})
    submit = SubmitField("Add Room")

class AddTaskForm(FlaskForm):
    """ Add a new task to a room of a house. """
    name = StringField("Task Name", validators=[DataRequired()], render_kw={"placeholder": "Sweep floor"})
    frequency = IntegerField("Frequency (Days)", validators=[DataRequired()])
    points = IntegerField("Point Value", validators=[DataRequired()])
    submit = SubmitField("Add Task")