from flaskblog import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    images = db.Column(db.PickleType, nullable=True, default=None)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='comment_post', lazy=True)
    post_likes = db.relationship('PostLike', backref='post', lazy='dynamic')

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class PostLike(db.Model):
    __tablename__ = 'post_like'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)