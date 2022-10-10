from flask import Blueprint, render_template
from app.firstmodules.models import Pictures, Users
from app.database import db
from app import get_app
from config import Config
import os

removes = Blueprint('removes', __name__)

app = get_app()
app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER


@removes.route('/delete_image/<path:user_login>/<path:filename>')
def delete_image(user_login, filename):
    image = Pictures.query.filter_by(filename=filename).first()
    user_info = Users.query.all()
    filename = image.filename

    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    image = Pictures.query.filter_by(filename=filename).delete()
    db.session.commit()

    return render_template('response/success_remove.html', title=filename, user_info=user_info)
