from wtforms import StringField, SubmitField
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms.fields.simple import TextAreaField, MultipleFileField
from flask_wtf.file import FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    files_upload = MultipleFileField('Update Images', validators=[FileAllowed(['jpg', 'png', 'jpeg','mp4'])])
    submit = SubmitField('Post')
    
    
class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')