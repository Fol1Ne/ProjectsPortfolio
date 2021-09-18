from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import secure_filename
from app import app, db
from app.forms import RegistrationForm, LoginForm, EditProfileForm
from app.models import User
import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

@app.route("/")
def home():
    try:
        avatar = current_user.avatar
    except:
        avatar = "/static/images/defaultAvatar.png"
    return render_template("home.html", title="Home", avatar=avatar)

@app.route("/profile")
def profile():
    print(current_user.avatar)
    return render_template("profile.html", title="Profile", user=current_user, avatar=current_user.avatar)

@app.route("/editProfile", methods=["GET", "POST"])
def editProfile():
    form = EditProfileForm()
    if form.validate_on_submit():
        newAvatar = form.avatar.data
        if (newAvatar):
            current_user.avatar = ("/static/images/avatar" + current_user.username + ".jpg")
            newAvatar.save(os.path.join(BASEDIR, "static", "images", ("avatar" + current_user.username + ".jpg")))
        current_user.gender = form.gender.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for("editProfile"))
    elif request.method == "GET":
        form.about_me.data = current_user.about_me
        form.gender.data = current_user.gender
    return render_template("editProfile.html", title="Edit Profile", user=current_user, form=form, avatar=current_user.avatar)

@app.route("/registration", methods=["GET", "POST"])
def registration():
    form = RegistrationForm()
    if current_user.is_authenticated:
        return redirect("/")
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("registration.html", title="Registration", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect("/")
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            return redirect("/login")
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for("home"))
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))