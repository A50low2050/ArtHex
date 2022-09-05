
from flask import Blueprint, render_template, redirect, url_for, request, make_response
from flask_login import logout_user, login_required, current_user
from app.firstmodules.models import Users, Profiles, Pictures
from app import get_app
from app.database import db


module = Blueprint('module', __name__)


@module.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('module.profile'))

    return render_template('authorization.html', title='authorization')


@module.route('/profile')
@login_required
def profile():
    user_info = Users.query.all()
    data_user = Users.query.first()

    user_pictures = Pictures.query.all()
    count_content = Pictures.query.count()

    return render_template('profile.html', title='Мой профиль',
                           user_info=user_info,
                           data_user=data_user,
                           user_pictures=user_pictures,
                           count_content=count_content,
    )


@module.route('/userava')
def userava():
    img = None
    profiles = Profiles.query.first()
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
            return redirect(url_for('module.profile'))

        update_avatar = Profiles.query.first()
        update_avatar.image = avatar.read()
        db.session.commit()

    return redirect(url_for('module.profile'))


@module.route('/logout')
def logout():
    logout_user()
    return render_template('authorization.html', title='Авторизация')
