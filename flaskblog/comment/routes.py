from flask import Blueprint, redirect, url_for, jsonify, request, render_template
import flaskblog

from flaskblog.models.ReplyModel import Reply
from flaskblog.reply.form import ReplyForm
from .forms import CommentForm
from flaskblog.models.PostModel import Post
from flaskblog.models.CommentModel import Comment
from flaskblog import db, logger
from flask_login import login_required, current_user
comment = Blueprint('comments', __name__)

@comment.route('/comment/<int:id>')
@login_required
def home_comment(id):
    post = Post.query.get_or_404(id)
    logger.info('User {} redirected to post {}'.format(current_user.get_id(), post.id))
    return redirect(url_for('posts.post'))


@comment.route('/comment/new/<int:post_id>', methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, post_id=post_id, author_id=current_user.id)
        db.session.add(comment)
        db.session.commit()
        logger.info('user {} commented on {}'.format(current_user.get_id(), post_id))
        return redirect(url_for('posts.post', post_id=post_id))
    else:
        return redirect(url_for('main.home'))
    

@comment.route('/post/comment/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def single_comment(comment_id):
    form = ReplyForm()
    comment = Comment.query.get_or_404(comment_id)
    page = request.args.get('page', 1, type=int)
    replies = Reply.query.filter_by(comment_id=comment_id).order_by(Reply.date.desc()).paginate(per_page=2,page=page)
    return render_template('comment.html',replies=replies , comment = comment, form =form)




@comment.route('/actioncomment/<int:comment_id>/<action>')
@login_required
def action_like(comment_id,action):
    comment = Comment.query.filter_by(id = comment_id).first_or_404()
    if action == "like":
        print("Like")
        current_user.like_comment(comment)
        db.session.commit()
    if action == 'unlike':
        print("Unlike")
        current_user.unlike_comment(comment)   
        db.session.commit()
    return redirect(request.referrer)