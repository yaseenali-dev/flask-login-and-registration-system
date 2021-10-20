from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField(
        "name", validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"}
    )
    password = PasswordField(
        "password", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    remember_me = BooleanField("remember me")


class SignupForm(FlaskForm):
    name = StringField(
        "name",
        validators=[DataRequired(), Length(min=3)],
        render_kw={"placeholder": "Name"},
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            EqualTo("password_confirm", message="Password must match"),
            Length(min=8),
        ],
        render_kw={"placeholder": "Password"},
    )

    password_confirm = PasswordField(
        "Confirm",
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Confirm"},
    )


class ForgotPasswordForm(FlaskForm):
    email = StringField(
        "email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"},
    )


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
            EqualTo("password_confirm", message="Password must match"),
            Length(min=8),
        ],
        render_kw={"placeholder": "Password"},
    )

    password_confirm = PasswordField(
        "Confirm",
        validators=[DataRequired(), Length(min=8)],
        render_kw={"placeholder": "Confirm"},
    )
