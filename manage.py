from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from data import get_lectures
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

    soup = get_lectures()
    links = []
    titles = []

    for link in soup.find_all('a'):
        links.append('http://curric.rithmschool.com/r13/lectures/' +
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
            titles.append(soup.title.string)

    db.session.commit()


def get_all_exercies():

    soup = get_lectures()
    links = []
    titles = []

    for link in soup.find_all('a'):
        links.append('http://curric.rithmschool.com/r13/exercies/' +
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
            titles.append(soup.title.string)

    db.session.commit()


if __name__ == '__main__':
    manager.run()