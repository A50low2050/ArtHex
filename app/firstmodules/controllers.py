
from flask import Blueprint, render_template, redirect, url_for, request, make_response
from flask_login import logout_user, login_required, current_user
from app.firstmodules.models import Users, Profiles, Pictures
from app import get_app
from app.database import db


module = Blueprint('module', __name__)


@module.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('module.profile', user_login=current_user.login))

    return render_template('authorization.html', title='authorization')


@module.route('/profile/<path:user_login>')
def profile(user_login):
    data_user = Users.query.filter_by(login=user_login).first()
    user_pictures = Pictures.query.filter_by(user_id=current_user.id).all()

    count_content = Pictures.query.filter_by(user_id=current_user.id).count()

    return render_template('profile.html',
                           data_user=data_user,
                           user_pictures=user_pictures,
                           count_content=count_content,
                           title='profile',)


@module.route('/userava')
def userava():
    img = None
    profiles = Profiles.query.filter_by(user_id=current_user.id).first()
    avatar = profiles.image

    if avatar is None:
        app = get_app()

        with app.open_resource(app.root_path + url_for('static', filename='img/user.png'), 'rb') as file:
            img = file.read()

            h = make_response(img)
            h.headers['Content-type'] = 'image/png'
            return h

    h = make_response(avatar)
    h.headers['Content-type'] = 'image/png'
    return h


@module.route('/update_avatar', methods=(['POST']))
def update_avatar():
    if request.method == 'POST':
        avatar = request.files['file']

        if not avatar:
            return redirect(url_for('module.profile', user_login=current_user.login))

        update_avatar = Profiles.query.filter_by(user_id=current_user.id).first()

        update_avatar.image = avatar.read()
        db.session.commit()

    return redirect(url_for('module.profile', user_login=current_user.login))


@module.route('/logout')
def logout():
    logout_user()
    return render_template('authorization.html', title='Авторизация')
