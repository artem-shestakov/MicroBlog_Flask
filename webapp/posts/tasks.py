from webapp import celery
from flask import current_app
import smtplib
from .models import Reminder, db
from email.mime.text import MIMEText
from pytz import timezone


@celery.task(bind=True, ignore_result=True, default_retry_delay=300, max_retries=5)
def remind(self, pk):
    reminder = Reminder.query.get(pk)
    try:
        msg = MIMEText(reminder.text)
        msg["Subject"] = "Reminder from WebBlog"
        msg["From"] = current_app.config['SMTP_FROM']
        msg["To"] = reminder.email
        smtp_server = smtplib.SMTP(current_app.config['SMTP_SERVER'], 587)
        smtp_server.starttls()
        smtp_server.login(current_app.config['SMTP_USER'], current_app.config['SMTP_PASS'])
        smtp_server.sendmail("", [reminder.email], msg.as_string())
        smtp_server.close()
    except Exception as e:
        self.retry(exc=e)


@celery.task(bind=True)
def log(self, msg):
    try:
        print(msg)
        return msg
    except Exception as e:
        self.retry(exc=e)


def reminder_save(mapper, connect, self):
    tz = timezone("Europe/Moscow")
    eta = tz.localize(self.date)
    remind.apply_async(args=(self.id,), eta=eta)
