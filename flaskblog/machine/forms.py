from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.fields.core import IntegerField
from wtforms.validators import DataRequired
from wtforms.fields.simple import TextAreaField

class SentimentForm(FlaskForm):
    text = TextAreaField('Review', validators=[DataRequired()])
    result = StringField('Review Type')
    per = StringField('Accuracy Percentage')
    submit = SubmitField('Analyze')


class SummarizeForm(FlaskForm):
    text = TextAreaField('Original Text', validators=[DataRequired()])
    num = IntegerField('Number of Sentences', validators=[DataRequired()])
    summary = TextAreaField('Summary')
    submit = SubmitField('Summarize')