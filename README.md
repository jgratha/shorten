# Shorten

Hi there!
Shorten is webservice which can shorten urls like TinyURL and bit.ly

## Installation

Open a terminal and do the following steps.

```bash
cd <your-python-projects-folder>
git clone git@github.com:jgratha/shorten.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
flask db upgrade
```

## Running tests

To run the unittest execute the following line inside the project folder.

```bash
python -m unittest discover tests
```

## Running the webservice locally

To run the app execute the following line in the project folder.

```bash
flask run
```

## What would I have added with more time?

- Some measures to prevent redirect loops
- Some investigation to prevent generating existing shortcodes

## Sources used

- The project structure is inspired by the Flask mega tutorial by Miguel Grinberg
- The shortcode generator uses
- The shortcode regex validator was inspired by
- The url validator was inspired by, the django implentation
- The errorhandler was inspired by 
 