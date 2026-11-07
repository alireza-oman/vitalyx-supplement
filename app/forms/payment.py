from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileRequired, FileAllowed


class PaymentForm(FlaskForm):
    tracking_number = StringField(
        "Bank Transaction Reference Number",
        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    receipt_image = FileField(
        "Payment Receipt",
        validators=[
            FileRequired(),
            FileAllowed(
                ["jpg", "jpeg", "png", "webp"],
                "Only image files are allowed."
            )
        ]
    )

    submit = SubmitField("Submit Payment")