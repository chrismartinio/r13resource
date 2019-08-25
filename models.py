"""Models for r13 resource"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    """ Connect to Database """

    db.app = app
    db.init_app(app)


class Lecture(db.Model):
    """ Lecture """

    __tablename__ = 'lectures'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)


class Exercise(db.Model):
    """ Exercise """

    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(300), nullable=False)


class GitUser(db.Model):
    """ GitHub Users """

    __tablename__ = 'gitusers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner_name = db.Column(db.Text, nullable=False)
    owner_url = db.Column(db.Text, nullable=False)
    owner_avatar = db.Column(db.Text, nullable=False)


class GitRepo(db.Model):
    """ GitHub Repos """

    __tablename__ = 'gitrepos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    repo_name = db.Column(db.Text, nullable=False)
    repo_url = db.Column(db.Text, nullable=False)
    repo_created = db.Column(db.Text, nullable=False)
    repo_last_push = db.Column(db.Text, nullable=False)
    repo_git_url = db.Column(db.Text, nullable=False)
    repo_size = db.Column(db.Text, nullable=False)
    repo_owner = db.Column(db.Text, nullable=False)
