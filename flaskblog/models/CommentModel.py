from flaskblog import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comment_likes = db.relationship('CommentLike', backref='post',  cascade = "all,delete-orphan", lazy='dynamic')
    reply = db.relationship('Reply', backref='comment_reply', cascade = "all,delete-orphan", lazy=True)

    def __repr__(self):
        return f"Comment({self.id})"


class CommentLike(db.Model):
    __tablename__ = 'comment_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)