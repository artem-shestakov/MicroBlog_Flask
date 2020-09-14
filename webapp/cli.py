import logging
import click
from flask.cli import AppGroup
from .auth.models import User, Role, db

log = logging.getLogger(__name__)


def register(app):
    """Register CLI commands for application"""
    create_cli = AppGroup("create")
    list_cli = AppGroup("list")
    init_cli = AppGroup("init")

    @create_cli.command("user")
    @click.option("--email", prompt="User's email address", help="User's email address")
    @click.option("--f_name", prompt="User's first name", help="User's first name")
    @click.option("-p", "--password", prompt="Enter password", hide_input=True, confirmation_prompt=True,
                  help="Password for user")
    @click.option("-a", "--administrator", is_flag=True, help="Use for create administrator")
    def create_user(email, f_name, password, administrator):
        """Create user. If -a set, user will have Administrator right"""
        user = User(email=email, f_name=f_name)
        user.set_password(password)
        try:
            if administrator:
                admin_role = Role.query.filter_by(name="administrator").one()
                user.roles.append(admin_role)
            db.session.add(user)
            db.session.commit()
            click.echo(f"User {email} added.")
            log.info(f"User {email} added.")
        except Exception as err:
            log.error(f"Fail to add user: username {email} Error {err}")
            db.session.rollback()

    @list_cli.command("users")
    def list_users():
        """List of app's users"""
        try:
            log.info("Getting the list of users")
            users = User.query.all()
            click.echo(f"{'ID':4}{'Username':30}{'User`s roles'}")
            for user in users:
                click.echo(f"{user.id:<4}{user.email:<30}{user.roles}")
        except Exception as err:
            log.error(f"Error with getting the list of users. Error {err}")

    @list_cli.command("routes")
    def list_routes():
        """List of all app's routes"""
        click.echo(f"{'URLs':50}{'Method':50}")
        for url in app.url_map.iter_rules():
            click.echo(f"{url.rule:<50} {url.methods}")

    @init_cli.command("database")
    def init_db():
        """Create database roles and blog roles"""
        for num, role in enumerate(app.config["USER_ROLES"]):
            user_role = Role(name=role["name"])
            user_role.description = role["description"]
            try:
                if num == 0:
                    db.create_all()
                    click.echo("All tables has been created")
                db.session.add(user_role)
                db.session.commit()
                click.echo(f"Role '{role['name']}' has been added")
            except Exception as err:
                db.session.rollback()
                log.error(f"Error with creating DB tables {err}")

    # Add CLI group
    app.cli.add_command(create_cli)
    app.cli.add_command(list_cli)
    app.cli.add_command(init_cli)
