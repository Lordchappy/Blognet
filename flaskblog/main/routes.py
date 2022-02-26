from flask import Blueprint, render_template, request
from flaskblog.models.PostModel import Post
from flaskblog import logger
from flask_login import login_required, current_user
main = Blueprint('main', __name__)

@main.route('/about')
def about():
    logger.debug('user {} route to about page'.format(current_user.get_id()))
    return render_template('about.html', title='About')


@main.route('/')
@main.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    logger.debug('user {} routed to home page'.format(current_user.get_id()))
    return render_template('home.html', posts=posts, state='home')


@main.route('/search/post', methods=['GET', 'POST'])
@login_required
def search():
    page = request.args.get('page', 1, type=int)
    keyword = request.form['keyword']
    search = '%{}%'.format(keyword)
    posts = Post.query.filter(Post.title.ilike(search) | Post.content.contains(search)).paginate(per_page=5, page=page)
    logger.debug('user {} search with keyword {} to about page'.format(current_user.get_id(), keyword))
    return render_template('home.html', posts=posts, keyword=keyword)