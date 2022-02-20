from flask import Blueprint, redirect, request, url_for
from .form import ReplyForm
from flaskblog.models.ReplyModel import Reply
from flaskblog import db, logger
from flask_login import login_required, current_user
reply = Blueprint('replies', __name__)

@reply.route('/reply/new/<int:comment_id>', methods=['GET', 'POST'])
@login_required
def new_reply(comment_id):
    form = ReplyForm()
    if form.validate_on_submit():
        reply = Reply(reply=form.reply.data, comment_id=comment_id, author_id=current_user.id)
        db.session.add(reply)
        db.session.commit()
        logger.info('user {} reply to comment {}'.format(current_user.get_id(), comment_id))
        return redirect(url_for('comments.single_comment', comment_id=comment_id))
    else:
        return redirect(url_for('main.home'))
    

@reply.route('/actionreply/<int:reply_id>/<action>')
@login_required
def action_like(reply_id,action):
    reply = Reply.query.filter_by(id = reply_id).first_or_404()
    if action == "like":
        print("Like")
        current_user.like_reply(reply)
        db.session.commit()
    if action == 'unlike':
        print("Unlike")
        current_user.unlike_reply(reply)   
        db.session.commit()
    return redirect(request.referrer)
    
    
    
    
