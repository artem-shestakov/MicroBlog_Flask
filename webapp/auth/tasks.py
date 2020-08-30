from flask import current_app, render_template
from webapp import celery
from email.mime.text import MIMEText
from .utils import generate_confirm_token
import smtplib


@celery.task(bind=True, ignore_result=True, default_retry_dalay=300, max_retries=5)
def you_are_welcome(self, email, token):
    with current_app.app_context():
        msg = MIMEText(render_template("welcome.html", user=self, token=token), "html")
    msg["Subject"] = "Welcome from Web Blog"
    msg["From"] = "Web Blog"
    msg["To"] = email

    try:
        smtp_server = smtplib.SMTP(current_app.config['SMTP_SERVER'], 587)
        smtp_server.starttls()
        smtp_server.login(current_app.config['SMTP_USER'], current_app.config['SMTP_PASS'])
        smtp_server.sendmail("", [email], msg.as_string())
        smtp_server.close()
        return
    except Exception as e:
        self.retry(exc=e)


def welcome_sender(mapper, connection, self):
    token = generate_confirm_token(self.email)
    you_are_welcome.apply_async(args=(self.email, token,))
