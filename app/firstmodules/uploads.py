from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import send_from_directory
from flask_login import current_user
from config import Config
from werkzeug.utils import secure_filename
import os
from app import get_app
from app.firstmodules.models import Users, Pictures
from app.database import db
from app.firstmodules.forms import FormUploadImage
from sqlalchemy import exc

uploads = Blueprint('uploads', __name__)

app = get_app()
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER


def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


@uploads.route('/sumbission', methods=['POST', 'GET'])
def sumbission():
    form = FormUploadImage()

    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('Soory, I can not this file', category='alert alert-danger')
            return redirect(request.url)
        file = request.files['file']

        if file.filename == '':
            flash('Please, choose the file', category='alert alert-secondary')
            return redirect(request.url)
        if file and allowed_files(file.filename):
            filename = secure_filename(file.filename)

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            title = request.form['title']
            description = request.form['description']

            try:
                pictures = Pictures(title=title, description=description, filename=filename, user_id=current_user.id)
                db.session.add(pictures)
                db.session.commit()
                return redirect(url_for('module.profile', user_login=current_user.login))

            except exc.IntegrityError:
                flash('You already have this is image', category='alert alert-danger')
                db.session.rollback()

        else:
            flash('You have selected the wrong file resolution', category='alert alert-danger')
            return redirect(request.base_url)

    return render_template('uploads.html', title='Download Picture', form=form)


@uploads.route('/sumbission/<filename>')
def download_picture(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@uploads.route('/gallery/<path:user_login>/<path:filename>')
def gallery(user_login, filename):
    image = Pictures.query.filter_by(filename=filename).first()

    filename = image.filename
    id_image = image.id

    return render_template('gallery.html', title=filename,
                           filename=filename,
                           image=image,
                           id_image=id_image,
    )
