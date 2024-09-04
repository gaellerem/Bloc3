from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.posts import bp
from app.extensions import db
from app.models.post import Post
from app.webforms import PostForm

@bp.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

@bp.route('/post/create', methods=('GET', 'POST'))
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post = Post(title=title, content=content, user_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create_post.html', form=form)

@bp.route('/post/<int:post_id>/edit', methods=('GET', 'POST'))
@login_required
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        post.title = title
        post.content = content
        db.session.commit()
        return redirect(url_for('posts.post', post_id=post.id))
    form.title.data = post.title
    form.content.data = post.content
    return render_template('edit_post.html', post=post, form=form)


@bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash("L'article a bien été supprimé !", 'success')
    return redirect(url_for('index'))

