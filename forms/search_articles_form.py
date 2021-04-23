from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import DateField, SubmitField
from wtforms.validators import DataRequired


class SearchArticlesForm(FlaskForm):
    theme = StringField('Тема статьи', validators=[DataRequired()])
    submit = SubmitField('Поиск')