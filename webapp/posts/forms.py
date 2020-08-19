from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_babel import lazy_gettext as _l


# Comment Form
class CommentForm(FlaskForm):
    name = StringField(_l("Name"), validators=[DataRequired(), Length(max=255, message="This field can't be empty")])
    text = TextAreaField(_l(u"Comment"), validators=[DataRequired(message="This field can't be empty")])


class PostForm(FlaskForm):
    title = StringField(_l("Title"), validators=[DataRequired(), Length(max=255)])
    text = TextAreaField(_l("Content"), validators=[DataRequired()])
