from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import current_user, login_user

from app.firstmodules.forms import FormRegister
from app.firstmodules.models import Users, Profiles
from app.database import db


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('module.profile'))

    if request.method == 'POST':
        login = request.form['login']
        password = request.form['psw']

        user = Users.query.filter_by(login=login).first()
        remember_choose = True if request.form.get('remember') else False

        if user and check_password_hash(user.password, password):
            login_user(user, remember=remember_choose)

            return redirect(url_for('module.profile', user_login=user.login))
        else:
            flash('invalid login/password pair', category='alert alert-danger')
            return redirect(url_for('auth.login'))

    return render_template('authorization.html', title='Авторизация')


@auth.route('/register', methods=('POST', 'GET'))
def register():
    form = FormRegister()

    if form.validate_on_submit():
        login = request.form['login']
        email = request.form['email']
        hash = generate_password_hash(request.form['password'])

        check_email = Users.query.filter(Users.email == email).first()
        check_login = Users.query.filter(Users.login == login).first()

        if check_email:
            flash('This is email exists, please use different email', category='alert alert-danger')
            return redirect(url_for('auth.register'))

        elif check_login:
            flash('This is login exists, please use different login', category='alert alert-danger')
            return redirect(url_for('auth.register'))
        else:

            user = Users(login=login, email=email, password=hash)
            db.session.add(user)
            db.session.flush()

            profiles = Profiles(user_id=user.id)
            db.session.add(profiles)

            db.session.commit()

            return render_template('response/success.html', title='success')

    return render_template('register.html', title='Регистрация', form=form)

