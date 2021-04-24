from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired


class toures_form(FlaskForm):
    tour = StringField('Введи тур матчи которого надо показать', validators=[DataRequired()])
    submit = SubmitField('Применить')