from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask import send_from_directory
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


@uploads.route('/upload', methods=['GET', 'POST'])
def upload():
    form = FormUploadImage()
    user_info = Users.query.all()

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
                pictures = Pictures(title=title, description=description, filename=filename)
                db.session.add(pictures)
                db.session.commit()
                return redirect(url_for('module.profile'))

            except exc.IntegrityError:
                flash('You already have this is image', category='alert alert-danger')
                db.session.rollback()

        else:
            flash('You have selected the wrong file resolution', category='alert alert-danger')
            return redirect(request.url)

    return render_template('uploads.html', title='Download Picture', form=form, user_info=user_info)


@uploads.route('/upload/<filename>')
def download_picture(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@uploads.route('/gallery/<int:id>')
def gallery(id):
    image = Pictures.query.filter_by(id=id).first()
    user_info = Users.query.all()
    data_user = Users.query.first()

    filename = image.filename
    id_image = image.id

    return render_template('gallery.html', title=filename,
                           filename=filename,
                           user_info=user_info,
                           image=image,
                           id_image=id_image,
                           data_user=data_user
    )
