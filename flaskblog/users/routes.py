from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required, logout_user, login_user
from flaskblog import db, bcrypt, logger
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateForm, ResetPasswordForm, RequestRestForm, RequestVerifyForm
from flaskblog.models.UserModel import User
from flaskblog.models.PostModel import Post
from flaskblog.users.utils import send_reset_email, save_picture, send_login_notification_mail
users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account Created for {form.username.data} !. Kindly verify your account", 'success')
        logger.info(f"New user {user.username} created with id {user.id}")
        return redirect(url_for('users.verify_request', mail=user.email))
    return render_template('register.html', title='Register', form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        print(type(user.verified))
        if user.verified != 1:
            flash(' Kindly verify your Account!', 'info')
            return redirect(url_for('users.verify_request', mail=(user.email)))
        if bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            flash('You are logged in !', 'success')
            logger.info('User {} with user id {} successfully logged In'.format(user.username, user.id))
            return redirect(url_for('main.home'))
        flash('Login Unsuccessful. Kindly Confirm your Username and Password!', 'danger')
        logger.error('User {} login unsuccessful'.format(current_user.get_id()))
        logger.debug('User {} routed to login page'.format(current_user.get_id()))
    return render_template('login.html', title='Login', form=form)


@users.route('/logout')
def logout():
    user = current_user.get_id()
    logout_user()
    logger.info('User {} logout successfully'.format(user))
    return redirect(url_for('users.login'))


@users.route('/home/<string:username>')
@login_required
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    username = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=username).order_by(Post.date_posted.desc()).paginate(per_page=5,
      page=page)
    logger.info('User {} directed to users post'.format(username.id))
    return render_template('user_post.html', posts=posts, user=username)


@users.route('/verify_account', methods=['GET', 'POST'])
def verify_request():
    form = RequestVerifyForm()
    mail = request.args.get('mail')
    if mail:
        form.email.data = mail
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user.verified == 1:
            return redirect(url_for('users.login'))
        message_status = send_login_notification_mail(user)
        if message_status == 1:
            flash('An email has been sent to your email to verify your account', 'info')
            return redirect(url_for('users.login'))
        print(message_status)
        logger.info('Message sent to {} failed with error {}'.format(mail, message_status))
        flash('Email Failed! Retry verification again', 'danger')
        return redirect(url_for('users.verify_request', mail = mail))
    else:
        return render_template('verify.html', title='Account Verification', form=form)


@users.route('/verified/<token>')
def verify_token(token):
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or Expired token', 'warning')
        logger.error('User {} inpuuted an invalid or expired token'.format(current_user.get_id()))
        return redirect(url_for('users.verify_request'))
    else:
        user.verified = 1
        db.session.commit()
        flash('Your account has been verified and activated Successfully. Kindly login and explore', 'success')
        logger.info('User {} password successfuly updated'.format(current_user.get_id()))
        return redirect(url_for('users.login'))

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    else:
        form = RequestRestForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=(form.email.data)).first()
            send_reset_email(user)
            flash('An email has been sent to your email to reset password', 'info')
            logger.info(' User {} successfully reset password'.format(user.id))
            return redirect(url_for('users.login'))
        return render_template('reset_request.html', title='Reset Password', form=form)


@users.route('/reset_password/<token>')
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Invalid or Expired token', 'warning')
        logger.error('User {} inpuuted an invalid or expired token'.format(current_user.get_id()))
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated. Kindly login ', 'success')
        logger.info('User {} password successfuly updated'.format(current_user.get_id()))
        return redirect(url_for('users.login'))
    else:
        return render_template('reset_token.html', title='Reset Password', form=form)


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            image = save_picture(form.picture.data)
            current_user.image_file = image
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Information was Successfully Updated ', 'success')
        logger.info('user {} information successfully updated'.format(current_user.get_id()))
        return redirect(url_for('users.account'))
    else:
        if request.method == 'GET':
            form.username.data = current_user.username
            form.email.data = current_user.email
        image = url_for('static', filename=('imagefolder/' + current_user.image_file))
        return render_template('account.html', title='Account', image=image, form=form)