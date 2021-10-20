from flask import current_app, url_for, render_template
from .app import mail
from flask_mail import Message
from threading import Thread

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, token):
    app = current_app._get_current_object()
    msg = Message(subject,
                    sender=app.config['MAIL_USERNAME'],
                    recipients=[to.email])
    msg.html = render_template(template, token=token, to=to)
    thr = Thread(target=send_async_mail, args=[app, msg])
    thr.start()
    return thr
