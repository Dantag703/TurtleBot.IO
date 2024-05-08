from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()], render_kw={'placeholder': 'Username', 'autocorrect': 'off', 'autocomplete': 'off'})
    password = PasswordField(validators=[DataRequired()], render_kw={'placeholder': 'Password', 'autocorrect': 'off', 'autocomplete': 'off'})
    submit = SubmitField('Login')

class SignUpForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pswd = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Enviar')

class TodoForm(FlaskForm):
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Crear')


class DeleteTodoForm(FlaskForm):
    submit = SubmitField('Borrar')


class UpdateTodoForm(FlaskForm):
    submit = SubmitField('Actualizar')
