from ctypes import sizeof
from itertools import count
from flask import Blueprint, request, render_template, redirect, abort, url_for, flash
import os
from flaskblog.comment.forms import CommentForm
from flaskblog.models.CommentModel import Comment
from flaskblog.models.PostModel import Post
from flaskblog.posts.forms import PostForm, UpdateForm
from flaskblog import db, logger,app
from flask_login import current_user, login_required

posts = Blueprint('posts', __name__)

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
    
        if len(form.files_upload.data) > 2:
            form.files_upload.data = None
            flash('Maximum of Images Exceeeded ', 'info')
            return render_template('create_post.html', title='New Post', form=form, legend='New Post')
        
        post = Post(title=form.title.data, content=form.content.data, author=current_user, images=None)
        db.session.add(post)
        db.session.commit()
    
        file_uploaded = str(form.files_upload.data)
        if file_uploaded.__contains__("image") or file_uploaded.__contains__("video"):
            if form.files_upload.data:
                file_names =[]
                files = request.files.getlist(form.files_upload.name)
                for num,file in enumerate(files):
                    file_content =  file.stream.read()
                    _, ext = os.path.splitext(file.filename)
                    filename = "Post{}-{}{}".format(post.id,str(num),str(ext).lower())
                    with open(os.path.join(app.root_path, 'static/imagefolder', filename), 'wb') as f:
                        f.write(file_content)
                        file_names.append(filename)   
                post.images = file_names
                db.session.commit()
        flash(' Your post has been created ', 'success')
        logger.info('user {} created a new post with post id [{}]'.format(current_user.get_id(), post.id))
        return redirect(url_for('main.home'))
    else:
        return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post(post_id):
    form = CommentForm()
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date.desc()).paginate(per_page=2,
      page=page)
    logger.debug('user {} route to post page with id [{}]'.format(current_user.get_id(), post.id))
    return render_template('post.html', title=post.title, post=post, comments=comments, form=form)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        logger.error('user {} cannot update post {}'.format(current_user.get_id(), post.id))
        abort(403)
    form = UpdateForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        logger.info('User {} successfully updated post {}'.format(current_user.get_id(), post.id))
        return redirect(url_for('posts.post', post_id=(post.id)))
    else:
        if request.method == 'GET':
            form.title.data = post.title
            form.content.data = post.content
        return render_template('update_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        logger.error('user {} cannot delete post {}'.format(current_user.get_id(), post.id))
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    logger.info('user {} Successfully deleted post {}'.format(current_user.get_id(), post.id))
    return redirect(url_for('main.home'))

@posts.route('/actionpost//<action>/<int:post_id>')
@login_required
def action_like(action,post_id):
    post = Post.query.filter_by(id = post_id).first_or_404()
    if action == "like":
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)