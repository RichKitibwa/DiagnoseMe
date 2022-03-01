import click
from config import db
from models import User


def create_db():
    """Creates database"""
    db.create_all()


def drop_db():
    """Cleans database"""
    db.drop_all()


def create_model_table():
    """ Create table model in the database """
    User.__table__.create(db.engine)


def init_app(app):
    # add multiple db commands
    for command in [create_db, drop_db, create_model_table]:
        app.cli.add_command(app.cli.command()(command))
