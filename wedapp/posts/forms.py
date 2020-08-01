from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


# Comment Form
class CommentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=255, message="This field can't be empty")])
    text = TextAreaField(u'Comment', validators=[DataRequired(message="This field can't be empty")])


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(max=255)])
    text = TextAreaField("Content", validators=[DataRequired()])
