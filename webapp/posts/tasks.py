from webapp import celery
from webapp.auth.models import User
from celery import group
from flask import current_app, render_template
import smtplib
from .models import Reminder, db, Post
from email.mime.text import MIMEText
import datetime
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


@celery.task(bind=True, ignore_result=True, default_retry_dalay=300, max_retries=5)
def week_digest(self, email):
    """Send week digest of posts"""
    # Getting current day and week day
    current_day = datetime.datetime.now()
    week_day = current_day.weekday()
    # Getting monday date
    start = current_day - datetime.timedelta(days=week_day)
    start = datetime.date(start.year, start.month, start.day)
    # Getting sunday date
    end = start + datetime.timedelta(days=6)

    posts = Post.query.filter(Post.publish_date >= start, Post.publish_date <= end).all()
    if len(posts) == 0:
        return

    with current_app.app_context():
        msg = MIMEText(render_template("digest.html", posts=posts), "html")
    msg["Subject"] = "Weekly digest"
    msg["From"] = "WebBlog Weekly Digest"
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


@celery.task()
def week_digest_sender():
    """Start group of task for sending week digest"""
    users = User.query.filter_by(subscription=True).all()
    sig = group(week_digest.s(user.email) for user in users)
    result = sig.delay()
    result.get()


def reminder_save(mapper, connect, self):
    tz = timezone("Europe/Moscow")
    eta = tz.localize(self.date)
    remind.apply_async(args=(self.id,), eta=eta)
