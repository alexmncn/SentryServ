"""Forms section."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[InputRequired()])
    password = PasswordField('Contraseña', validators=[InputRequired()])


class LoginForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[InputRequired()])
    password = PasswordField('Contraseña', validators=[InputRequired()])


class CredentialsForm(FlaskForm):
    site = StringField('Sitio Web', validators=[InputRequired(), Length(max=255)])
    user = StringField('Usuario', validators=[Length(max=50)])
    email = StringField('Correo Electrónico', validators=[Email(), Length(max=255)])
    password = PasswordField('Contraseña', validators=[InputRequired(), Length(max=255)])
    description = StringField('Descripción', validators=[Length(max=255)])
