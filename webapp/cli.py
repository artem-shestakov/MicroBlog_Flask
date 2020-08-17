import logging
import click
from .auth.models import User, db

log = logging.getLogger(__name__)


def register(app):
    @app.cli.command("create-user")
    @click.argument("username")
    @click.argument("password")
    def create_user(username, password):
        user = User(username=username)
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            click.echo(f"User {username} added.")
            log.info(f"User {username} added.")
        except Exception as err:
            log.error(f"Fail to add user: username {username} Error {err}")
            db.session.rollback()

    @app.cli.command("list-users")
    def list_users():
        try:
            log.info("Getting the list of users")
            users = User.query.all()
            click.echo(f"{'ID':4}{'Username':30}{'User`s roles'}")
            for user in users:
                click.echo(f"{user.id:<4}{user.username:<30}{user.roles}")
        except Exception as err:
            log.error(f"Error with getting the list of users. Error {err}")

    @app.cli.command("list-routes")
    def list_routes():
        for url in app.url_map.iter_rules():
            click.echo(f"{url.rule} {url.methods} {url.endpoint}")