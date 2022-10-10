from flask import Blueprint, render_template, request
from app.firstmodules.models import Users, Pictures
from app.database import db


updates = Blueprint('updates', __name__)


@updates.route('/edit/<path:user_login>/<path:filename>')
def edit_image(user_login, filename):
    images = Pictures.query.filter_by(filename=filename).first()

    title = images.title
    description = images.description
    filename = images.filename
    id_image = images.id

    return render_template('editimage.html',
                           title=title,
                           description=description,
                           id_image=id_image,
                           filename=filename
    )


@updates.route('/update/<path:user_login>/<path:filename>', methods=['GET', 'POST'])
def update_image(user_login, filename):
    image = Pictures.query.filter_by(filename=filename).first()

    user_info = Users.query.all()
    data_user = Users.query.first()

    filename = image.filename
    id_image = image.id

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']

        images = Pictures.query.filter_by(filename=filename).update({
            'title': title,
            'description': description,
        })

        db.session.commit()

        return render_template('gallery.html', title=filename,
                               filename=filename,
                               user_info=user_info,
                               image=image,
                               id_image=id_image,
                               data_user=data_user
        )
