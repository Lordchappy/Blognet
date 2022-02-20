from flaskblog import db
from datetime import datetime

class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reply = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    likes = db.relationship('ReplyLike', backref='reply', lazy='dynamic')

    def __repr__(self):
        return str(self.id)


class ReplyLike(db.Model):
    __tablename__ = 'reply_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reply_id = db.Column(db.Integer, db.ForeignKey('reply.id'), nullable=False)