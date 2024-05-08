from flask import render_template, session, redirect, flash, url_for
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash

from app.forms import LoginForm, SignUpForm

from . import auth
from app.models import UserModel, UserData
global password, username

username = "nicolas"
password = "holahola"

@auth.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    context = {
        'login_form': login_form
    }

    if login_form.validate_on_submit():
        flash('gracia gei 2')
        usernamel = login_form.username.data
        passwordl = login_form.password.data
        
        if usernamel == username:
            if passwordl == password:
                user_data = UserData(usernamel, passwordl)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')

                redirect(url_for('home'))
            else:
                flash('La información no coincide')
        else:
            flash('El usuario no existe')
        flash('gracia gei')
        return redirect(url_for('index'))

    return render_template('login1.html', **context)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignUpForm()
    context = {
        'signup_form': signup_form
    }

    if signup_form.validate_on_submit():
        usernamen = signup_form.username.data
        passwordn = signup_form.password.data

        if usernamen != username:
            username = usernamen
            password = passwordn
            user_data = UserData(username, password)
            user = UserModel(user_data)
            login_user(user)

            flash('Bienvenido!')

            return redirect(url_for('home'))

        else:
            flash('El usuario existe!')

    return render_template('login1.html', **context)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))