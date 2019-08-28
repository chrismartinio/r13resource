from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask import json
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from models import Lecture, Exercise, Timestamp, GitUser, GitRepo, LocalUser
import requests
from config import ProductionConfig
from datetime import datetime, time
from data import parse_data

from models import db
from app import app

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def get_all_lectures():

    response = requests.get('https://curric.rithmschool.com/r13/lectures/')
    soup = BeautifulSoup(response.text)
    links = []

    # Drop current lecture table
    engine = create_engine(ProductionConfig.SQLALCHEMY_DATABASE_URI)
    Lecture.__table__.drop(engine)
    db.create_all()

    # Set up current lectures
    current_lectures = []
    for lecture in Lecture.query.all():
        current_lectures.append(lecture.title)

    for link in soup.find_all('a'):
        links.append('https://curric.rithmschool.com/r13/lectures/' +
                     link.get('href'))

    for link in links:
        if 'zip' in link:
            continue
        response = requests.get(link)
        soup = BeautifulSoup(response.text)
        if (soup.title is None):
            continue
        else:
            new_lecture = Lecture(title=soup.title.string, url=link)
            db.session.add(new_lecture)

    db.session.commit()


@manager.command
def get_all_exercises():

    response = requests.get('https://curric.rithmschool.com/r13/exercises/')
    soup = BeautifulSoup(response.text)
    links = []

    # Drop Exercise table
    engine = create_engine(ProductionConfig.SQLALCHEMY_DATABASE_URI)
    Exercise.__table__.drop(engine)
    db.create_all()

    # Set up current exercises to test for duplicates
    current_exercises = []
    for exercise in Exercise.query.all():
        current_exercises.append(exercise.title)

    for link in soup.find_all('a'):
        links.append('https://curric.rithmschool.com/r13/exercises/' +
                     link.get('href'))

    for link in links:
        if 'zip' in link:
            continue
        response = requests.get(link)
        soup = BeautifulSoup(response.text)
        if (soup.title is None):
            continue
        else:
            new_exercise = Exercise(title=soup.title.string, url=link)
            db.session.add(new_exercise)

    db.session.commit()


@manager.command
def update_repos():
    current_time = datetime.now()
    new_time = (current_time.strftime("%c"))

    # Drop tables
    engine = create_engine(ProductionConfig.SQLALCHEMY_DATABASE_URI)
    GitRepo.__table__.drop(engine)
    GitUser.__table__.drop(engine)

    db.create_all()

    # Update users
    users = LocalUser.query.all()
    timezone = {'Time-Zone':'PST8PDT'}
    for user in users:
        username = user.localuser
        git_data = requests.get(
            f'https://api.github.com/users/{username}/events', params=timezone)
        content = git_data.content
        parsed_json = json.loads(content)
        parse_data(parsed_json)

    # Timestamp update
    engine = create_engine(ProductionConfig.SQLALCHEMY_DATABASE_URI)
    Timestamp.__table__.drop(engine)
    db.create_all()

    new_timestamp = Timestamp(time=new_time)

    db.session.add(new_timestamp)
    db.session.commit()


if __name__ == '__main__':
    manager.run()

    # # Set up current exercises to test for duplicates
    # current_exercises = []
    # for exercise in Exercise.query.all():
    #     current_exercises.append(exercise.title)

    # for link in soup.find_all('a'):
    #     links.append('https://curric.rithmschool.com/r13/exercises/' +
    #                  link.get('href'))

    # for link in links:
    #     if 'zip' in link:
    #         continue
    #     response = requests.get(link)
    #     soup = BeautifulSoup(response.text)
    #     if (soup.title is None):
    #         continue
    #     else:
    #         if soup.title.string in current_exercises:
    #             continue
    #         else:
    #             new_exercise = Exercise(title=soup.title.string, url=link)
    #             db.session.add(new_exercise)