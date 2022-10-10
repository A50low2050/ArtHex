from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileRequired
from wtforms.validators import Length, Email, DataRequired, EqualTo


class FormRegister(FlaskForm):
    login = StringField('Login', validators=[Length(min=1, max=15)], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter Login',
    })
    email = EmailField('Email address', validators=[Email('Invalid email address')], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter Email',
    })
    password = PasswordField('Password', validators=[DataRequired(), Length(min=3, max=50)], render_kw={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    })
    password_repeat = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password'), Length(min=3, max=50)], render_kw={
            'class': 'form-control',
            'placeholder': 'Enter Repeat Password',
        })
    submit = SubmitField('Sign Up', render_kw={
        'class': 'btn btn-primary mt-3',
    })


class FormUploadImage(FlaskForm):
    title = StringField('Title', validators=[Length(max=50)], render_kw={
        'class': 'form-control',
        'id': 'name_file',
    })

    description = TextAreaField('Description', render_kw={
        'class': "form-control",
    })

    file = FileField(validators=[FileRequired()], render_kw={
        'class': "form-control-file",
        'id': "UploadInp",
    })

    submit = SubmitField('Submit', render_kw={
        'class': 'btn btn-primary mb-5',
    })
