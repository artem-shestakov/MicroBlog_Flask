from flask import current_app, render_template
from webapp import celery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .utils import generate_confirm_token, generate_reset_pass_token
import smtplib
import base64


@celery.task(bind=True, ignore_result=True, default_retry_dalay=300, max_retries=5)
def send_email(self, email, token, msg_type):
    """Send greeting and email confirmation email when new user add to database"""

    with current_app.app_context():
        if msg_type == "greeting":
            msg = MIMEMultipart("alternative")
            logo = base64.b64encode(open("./webapp/static/images/logo.png", "rb").read()).decode()
            part = MIMEText(render_template("welcome.html", user=self, token=token, logo=logo), "html")
            msg.attach(part)
            msg["Subject"] = "Welcome from MicroBlog"
        elif msg_type == "email_confirm":
            msg = MIMEText(render_template("email_confirm.html", user=self, token=token), "html")
            msg["Subject"] = "Email confirmation"
        elif msg_type == "reset_password":
            msg = MIMEText(render_template("reset_pass_email.html", token=token), "html")
            msg["Subject"] = "Password reset MicroBlog"
    msg["From"] = "MicroBlog"
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


def greeting_sender(mapper, connection, self):
    token = generate_confirm_token(self.email)
    send_email.apply_async(args=(self.email, token, "greeting"))


def send_confirm_email(email):
    token = generate_confirm_token(email)
    send_email.apply_async(args=(email, token, "email_confirm"))


def send_pass_reset_email(email):
    token = generate_reset_pass_token(email)
    send_email.apply_async(args=(email, token, "reset_password"))
