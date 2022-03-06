from flaskblog import app
from flaskblog.models.CommentModel import Comment
from flaskblog.models.PostModel import PostLike

def post_number_of_likes(post):
    return PostLike.query.filter(PostLike.post_id == post.id).count()

def number_of_comments(post):
    return Comment.query.filter(Comment.post_id == post.id).count()

app.jinja_env.globals.update(
    
    post_number_of_likes = post_number_of_likes,
    number_of_comments = number_of_comments,
)