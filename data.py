import requests
from bs4 import BeautifulSoup

# Get request for lectures


def get_lectures():
    response = requests.get('http://curric.rithmschool.com/r13/lectures/')
    soup = BeautifulSoup(response.text)

    return soup
