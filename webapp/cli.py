import logging
import click
from .auth.models import User, Role, db
from datetime import datetime

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

    @app.cli.command("init-db")
    def init_db():
        user_role = Role(name="user")
        user_role.description = "Microblog's user. Read only rights."
        try:
            db.create_all()
            click.echo("All tables has been created")
            db.session.add(user_role)
            db.session.commit()
            click.echo("Role 'user' has been added")
        except Exception as err:
            db.session.rollback()
            log.error(f"Error with creating DB tables {err}")

    @app.cli.command("create-admin")
    def create_admin():
        admin_role = Role(name="administrator")
        admin = User(email="admin@admin.com", f_name="Administrator")
        admin.set_password("admin")
        admin.roles.append(admin_role)
        admin.email_confirm = True
        admin.email_confirm_on = datetime.now()
        try:
            db.session.add(admin)
            db.session.commit()
            click.echo("Administrator was added")
        except Exception as err:
            db.session.rallback()
            log.error(f"Error with creating administrator {err}")
