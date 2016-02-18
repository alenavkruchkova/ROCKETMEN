"""Utility file to seed ROCKETMEN database from Open Notify API data"""

from sqlalchemy import func
from model import Country
from model import Astronaut

from model import connect_to_db, db
from server import app

from bs4 import BeautifulSoup
import urllib

###########################################################################

# Pointing to url of the page I am going to scrape and parsing it with BeautifulSoup
r = urllib.urlopen('https://en.wikipedia.org/wiki/List_of_astronauts_by_first_flight').read()
soup = BeautifulSoup(r, "html.parser")

# Get all the rows from the tables on the webpage
rows = soup.find_all("tr")


# Get text between <td> tags
# and store necessary information in the list of lists
list_of_lists = []

rows = soup.find_all("tr")[1:552]

def get_name_date():
    """From table row get text in 2nd and 3rd colums"""

    for row in rows:
        cells = row.find_all("td")
        if cells:
            new_list = []
            new_list.append(cells[1].get_text())
            new_list.append(cells[2].get_text())
            list_of_lists.append(new_list)

def load_astronauts():
    """Load information from list_of_lists into database"""

    print "Astronauts"

    get_name_date()

    for item in list_of_lists:
        name, first_flight_start = item

        astronaut = Astronaut(name=name, first_flight_start=first_flight_start)

        # Add to the session
        db.session.add(astronaut)

    # Commit
    db.session.commit()


def load_countries():
    """Load countries from countres.csv into database."""

    print "Countries"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Country.query.delete()

    # Read countries.csv file and insert data
    for row in open("seed_data/output.txt"):
        r = row.splitlines()

    for rn in r:
        name, country_id = rn.split(",")

        country = Country(name=name, country_id=country_id)

        # Add to the session
        db.session.add(country)

    # Commit
    db.session.commit()


#####################################################################
if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import data

    load_countries()

    load_astronauts()
