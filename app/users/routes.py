from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from app.users import bp
from app.extensions import db
from app.models import User
from app.webforms import SignUpForm, LogInForm, EditUserForm, UpdatePasswordForm


@bp.route('/signup', methods=('GET', 'POST'))
def add():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = SignUpForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('users.dashboard'))
    return render_template('signup.html', form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LogInForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if user.verify_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                flash("Mot de passe incorrect", 'danger')
        else:
            flash("Identifiant inconnu", "danger")
    return render_template('login.html', form=form)


@bp.route('/logout', methods=('GET', 'POST'))
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route('/user/edit', methods=('GET', 'POST'))
@login_required
def update():
    form = EditUserForm(current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.dashboard'))
    form.username.data = current_user.username
    form.email.data = current_user.email
    return render_template('users/edit.html', form=form)


@bp.route('/user/edit/pass', methods=('GET', 'POST'))
@login_required
def update_pass():
    form = UpdatePasswordForm()
    if form.validate_on_submit():
        current_user.password = form.password.data
        db.session.commit()
        flash('Votre mot de passe a été mis à jour !', 'success')
        return redirect(url_for('users.dashboard'))
    return render_template('users/edit_pass.html', form=form)


@bp.route('/user/delete', methods=['POST', 'GET'])
@login_required
def delete():
    user = User.query.get_or_404(current_user.id)
    if user.is_admin:
        admin_count = User.query.filter_by(is_admin=True).count()
        if admin_count <= 1:
            flash("Impossible de supprimer le dernier administrateur.", "danger")
            return redirect(url_for('users.dashboard'))
    db.session.delete(user)
    db.session.commit()
    flash('Le profil a bien été supprimé.', 'success')
    return redirect(url_for('index'))


@bp.route('/dashboard')
@login_required
def dashboard():
    posts = current_user.posts
    return render_template('dashboard.html', posts=posts)
