from wtforms import SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.simple import TextAreaField

class ReplyForm(FlaskForm):
    reply = TextAreaField('reply', validators=[DataRequired()])
    submit = SubmitField('Post')