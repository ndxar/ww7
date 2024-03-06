from flask import Blueprint, render_template, request, flash, redirect, url_for, get_flashed_messages
from .models import User
from . import db, views
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():

    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.passwordHash, password):
                flash('Logeado', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Pass incorrecta', category='error')
        else:
            flash('email no existe', category='error')
            
    get_flashed_messages()

    return render_template('login.html', user=current_user)

@auth.route('/signup', methods=['GET','POST'])
def signup():

    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')   

        email_valido = re.match(r'[^@]+@[^@]+\.[^@]+', email)
        email_existe = User.query.filter_by(email=email).first()
        user_existe = User.query.filter_by(username=username).first()

        if not email_valido:
            flash('Mail invalido', category='error')
        elif email_existe:
            flash('El mal ya existe', category='error')
        elif user_existe:
            flash('El user ya existe', category='error')
        elif password1 != password2:
            flash('Las contraseñas no conciden', category='error')
        elif len(username) < 1:
            flash('Usuario muy corto', category='error')
        elif len(password1) < 10:
            flash('Pass muy corta', category='error')
        else:
            new_user = User(email=email, username=username, passwordHash=generate_password_hash(password1,method='SHA256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash('User creado')
            return redirect(url_for('views.home'))




    return render_template('signup.html', user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('logout.html', user=current_user)


@auth.route('/delete-account',methods=['GET','POST'])
@login_required
def deleteaccount():
    user=current_user
    if request.method == "POST":
        password = request.form.get('password')
        validation = request.form.get('validation') == "DEJAMEBORRARMICUENTA"

        if not check_password_hash(user.passwordHash, password):
            flash("Contraseña incorrecta",category="error")
            return redirect(url_for('views.settings'))
        elif not validation:
            flash("Código de validación no correcto",category="error")
            return redirect(url_for('views.settings'))
        else:
            flash("EL usuario ha sido borrado con éxito:(")
            User.query.filter_by(username=current_user.username).delete()
            db.session.commit()
            logout()
            
    return render_template('deleteaccount.html', user=current_user)
        