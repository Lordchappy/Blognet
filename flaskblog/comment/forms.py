from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.simple import TextAreaField, SubmitField

class CommentForm(FlaskForm):
    comment = TextAreaField('comment', validators=[DataRequired()])
    submit = SubmitField('Post')