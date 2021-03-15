# Shorten

Hi there!
Shorten is a webservice which can shorten urls like TinyURL and bit.ly

## Installation

Open a terminal and do the following steps.

```bash
cd <your-python-projects-folder>
git clone git@github.com:jgratha/shorten.git
cd shorten
python3 -m venv env
source env/bin/activate && pip install -r requirements.txt && source env/bin/activate
flask db upgrade
```

## Running tests

To run the unittests execute the following line inside the project folder.

```bash
python -m unittest discover tests
```

## Running the webservice locally

To run the app execute the following line in the project folder.

```bash
flask run
```

## What would I have added with more time?

- Some investigation and measures to prevent redirect loops
- Some investigation and a solution to prevent generating existing shortcodes

## Sources used

- The project structure is inspired by [the Flask mega tutorial by Miguel Grinberg](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
- The shortcode generator uses [the shortuuid package](https://github.com/skorokithakis/shortuuid)
- The shortcode regex validator is inspired by [this stackoverflow answer](https://stackoverflow.com/questions/57011986/how-to-check-that-a-string-contains-only-a-z-a-z-and-0-9-characters/57012038)
- The url validator is inspired by [this stackoverflow answer](https://stackoverflow.com/questions/7160737/how-to-validate-a-url-in-python-malformed-or-not)
- The errorhandler is inspired by https://flask.palletsprojects.com/en/1.1.x/errorhandling/ and https://flask.palletsprojects.com/en/1.1.x/patterns/apierrors/
 