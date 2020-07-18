from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired


class ResAdminLogin(FlaskForm):
    userName = StringField('userName', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')


class SimpleForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('submit')


class AddResalaCommittee(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    activity_id = SelectField('activity', validators=[DataRequired()], coerce=int)
    submit = SubmitField('submit')


class AddBot(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    url = StringField('url')
    activity_id = SelectField('activity', validators=[DataRequired()], coerce=int)
    submit = SubmitField('submit')
