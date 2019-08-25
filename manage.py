from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from bs4 import BeautifulSoup
from models import Lecture, Exercise
import requests

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
    current_lectures = Lecture.query.all()

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
            if (soup.title.string in current_lectures.title):
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


if __name__ == '__main__':
    manager.run()