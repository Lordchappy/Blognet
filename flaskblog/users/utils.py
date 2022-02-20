import os, secrets
from PIL import Image
from flask_mail import Message
from flaskblog import mail, app, logger
from flask import url_for

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/imagefolder', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def send_reset_email(user):
    try:
        token = user.get_reset_token()
        msg = Message('Password Reset Request', sender='noreply@demo.com',
          recipients=[
         user.email])
        msg.body = f"To verify_reset_token visit the following link:\n        {url_for('users.reset_token', token=token, _external=True)}\n\n        If you did not make this request then simply ignore this mail and no changes will be made to your account\n        "
        mail.send(msg)
        logger.info('message successfully sent to [{}] for reset mail  to user {}'.format(user.email, user.id))
    except Exception as err:
        logger.error('message failed for reset mail failed for user {} with {}'.format(user.id, err))



def send_login_notification_mail(user):
    try:
        token = user.get_reset_token()
        msg = Message('verification Request', sender='noreply@demo.com',
          recipients=[
         user.email])
        msg.body = f"To verify your account with blognet visit the following link:\n        {url_for('users.verify_token', token=token, _external=True)}\n\n        If you did not make this request then simply ignore this mail and no changes will be made to your account\n        "
        mail.send(msg)
        logger.info('message successfully sent to [{}] for verification to user {}'.format(user.email, user.id))
        return 1 
    except Exception as err:
        logger.error('message failed for reset mail failed for user {} with {}'.format(user.id, err))
        return 0
        