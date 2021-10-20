from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from .forms import LoginForm, SignupForm, ForgotPasswordForm, ResetPasswordForm
from ..models import User
from ..app import db
from flask_login import login_user, logout_user, login_required, current_user
from ..send_email import send_email
from functools import wraps

auth_blueprint = Blueprint("auth_blueprint", __name__)


@auth_blueprint.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for(".protected"))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(email=email).first()
        if user is not None and user.verify_password(password):
            login_user(user, remember=remember_me)
            next = session["next"]
            if next is None or not next.startswith("/"):
                next = url_for(".protected")
            session["next"] = ""
            return redirect(next)
        flash("wrong email or password", "error")
    return render_template("login.html", form=form)

@auth_blueprint.get("/unconfirmed")
def unconfirmed():
    return "unconfirmed"


@auth_blueprint.route("/register", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for(".protected"))
    form = SignupForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(name=name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            send_email(
                to=user,
                subject="Comfirm account",
                template="mail/confirm.html",
                token=user.generate_token(),
            )

            flash("check your email for confirmantion :)", "success")
            return redirect(url_for(".login"))
        flash("User Exist", "error")

    return render_template("signup.html", form=form)


@auth_blueprint.get("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for(".protected"))

    if current_user.confrim_token(token):
        db.session.commit()
        return redirect(url_for(".protected"))
    flash("token is expired or invalid")
    return redirect(url_for(".protected"))


@auth_blueprint.get("/confirm")
@login_required
def resend_confimation():
    if current_user.confirmed:
        return redirect(url_for(".protected"))
    user = current_user
    send_email(
        to=user,
        subject="Comfirm account",
        template="mail/confirm.html",
        token=user.generate_token(),
    )
    flash("New confirmation email has been send to your email.")
    return redirect(url_for(".protected"))


@auth_blueprint.route("/forgot_password", methods=["GET", "POST"])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for(".protected"))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_email(
                to=user,
                subject="Reset Password",
                template="mail/reset_password.html",
                token=user.generate_token(),
            )

            flash("check your email", "success")
            return redirect(url_for(".login"))
        flash("email not found", "error")
    return render_template("forgot_password.html", form=form)


@auth_blueprint.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for(".protected"))
    if not User.is_token_valid(token):
        flash(
            "token is invalid or expired, request another password reset request",
            "error",
        )
        return redirect(url_for(".forgot_password"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            return redirect(url_for(".login"))
        flash("token is not valid", "error")
        return redirect(".forgot_password")
    return render_template("reset_password.html", form=form)


@auth_blueprint.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))


@auth_blueprint.get("/protected")
@login_required
def protected(page=1):
    return render_template("protected.html")


# Ensure responses aren't cached
@auth_blueprint.after_request
def after_request(response):
    response.headers.add(
        "Cache-Control",
        "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
    )
    return response
