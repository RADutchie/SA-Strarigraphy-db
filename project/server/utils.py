# project/server/utils.py

from flask_mail import Message
from project.server import mail
from flask import render_template, current_app
from threading import Thread



def row2dict(row):
    """ Convert SQLAlchemy object to dict
    """
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))
    return d


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, sender, recipients, text_body, html_body):
    """ Helper function to send email
    """
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    Thread(target=send_async_email, args=(
        current_app._get_current_object(), msg)
        ).start()


def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('SA Strat db: Reset Your Password',
               sender=current_app.config.get('ADMIN_EMAIL'),
               recipients=[user.email],
               text_body=render_template('user/email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('user/email/reset_password.html',
                                         user=user, token=token))