from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class FriendsForm(FlaskForm):
    first_name = StringField('1 user:', validators=[DataRequired()])
    second_name = StringField('2 user:', validators=[DataRequired()])
    submit = SubmitField('Enter')
