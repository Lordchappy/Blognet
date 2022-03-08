from email.policy import default
from flaskblog import db, login_manager, app
from flaskblog.models.PostModel import PostLike
from flaskblog.models.CommentModel import Comment, CommentLike
from flaskblog.models.ReplyModel import Reply, ReplyLike
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, 
                           default='https://res.cloudinary.com/teamblog/image/upload/v1646713752/default_xfjzu9.jpg')
    password = db.Column(db.String(60), nullable=False)
    verified = db.Column(db.Integer, nullable = False, default = 0)
    
    posts = db.relationship('Post', 
                                    backref= 'author', 
                                    cascade = "all,delete-orphan",
                                    lazy=True)
    
    comments = db.relationship('Comment',
                                    backref='comment_author',
                                    cascade = "all,delete-orphan",
                                    lazy=True)
            
    reply = db.relationship('Reply',
                                    backref='reply_user', 
                                    cascade = "all,delete-orphan", 
                                    lazy=True)
            
    post_liked = db.relationship('PostLike',
                                    foreign_keys='PostLike.user_id',
                                    backref='user',
                                    cascade = "all,delete-orphan",
                                    lazy='dynamic')
        
    comment_liked = db.relationship('CommentLike',
                                    foreign_keys='CommentLike.user_id',
                                    backref='user',
                                    cascade = "all,delete-orphan",
                                    lazy='dynamic')
    reply_liked = db.relationship('ReplyLike',
                                    foreign_keys='ReplyLike.user_id',
                                    backref='user',
                                    cascade = "all,delete-orphan",
                                    lazy='dynamic')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    
    def is_verified(self):
        return self.verified

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return f"Invalid token or Wrong Token"
        return User.query.get(user_id)

    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)
            db.session.commit()

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(user_id= self.id, post_id=post.id).delete()
            db.session.commit()

    def has_liked_post(self, post):
        return PostLike.query.filter(PostLike.user_id == self.id, PostLike.post_id == post.id).count() > 0

    def number_of_comments(self, post):
        return Comment.query.filter(Comment.post_id == post.id).count()

    def post_number_of_likes(self, post):
        return PostLike.query.filter(PostLike.post_id == post.id).count()

    def like_comment(self, comment):
        if not self.has_liked_comment(comment):
            like = CommentLike(user_id=self.id, comment_id=comment.id)
            print("Hiijshkshks")
            db.session.add(like)
            db.session.commit()

    def unlike_comment(self, comment):
        if self.has_liked_comment(comment):
            CommentLike.query.filter_by(user_id=self.id, comment_id=comment.id).delete()
            db.session.commit()

    def has_liked_comment(self, comment):
        return CommentLike.query.filter(CommentLike.user_id == self.id, CommentLike.comment_id == comment.id).count() > 0

    def comment_number_of_likes(self, comment):
        return CommentLike.query.filter(CommentLike.comment_id == comment.id).count()

    def number_of_reply_for_comment(self, comment):
        return Reply.query.filter(Reply.comment_id == comment.id).count()

    def like_reply(self, reply):
        if not self.has_liked_reply(reply):
            reply = ReplyLike(user_id=self.id, reply_id=reply.id)
            db.session.add(reply)
            db.session.commit()

    def unlike_reply(self, reply):
        if self.has_liked_reply(reply):
            ReplyLike.query.filter_by(user_id=self.id, reply_id=reply.id).delete()
            db.session.commit()

    def has_liked_reply(self, reply):
        return ReplyLike.query.filter(ReplyLike.user_id == self.id, ReplyLike.reply_id == reply.id).count() > 0

    def reply_number_of_likes(self, reply):
        return ReplyLike.query.filter(ReplyLike.reply_id == reply.id).count()

    def __repr__(self):
        return f"User('{self.id}','{self.username}','{self.email}')"