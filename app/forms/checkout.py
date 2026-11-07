from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp

class CheckoutForm(FlaskForm):
    recipient_name = StringField(
        "Recipient Name",
        validators=[
            DataRequired(),
            Length(min=2, max=120),
        ],
    )

    phone = StringField(
        "Phone Number",
        validators=[
            DataRequired(),
            Length(min=7, max=20),
            Regexp(
                r"^[0-9+\-() ]+$",
                message="Enter a valid phone number.",
            ),
        ],
    )

    postal_code = StringField(
        "Postal Code",
        validators=[
            DataRequired(),
            Length(min=3, max=20),
        ],
    )

    shipping_address = TextAreaField(
        "Shipping Address",
        validators=[
            DataRequired(),
            Length(min=10, max=2000),
        ],
    )

    submit = SubmitField("Place Order")
