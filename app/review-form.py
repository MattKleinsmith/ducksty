from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class ReviewForm(FlaskForm):
    rating = StringField("Review this item", validators=[DataRequired()])
    review = TextAreaField("My review", validators=[DataRequired()])
    submit = SubmitField("Post My Review")
