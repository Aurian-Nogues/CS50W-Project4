# Project 4

Web Programming with Python and JavaScript

Youtube video: https://youtu.be/Xo5B9eB810o

This web app allows user to implement and monitor trade ideas.
The app is built in a Django framework using Python, HTML, CSS, SQL and Javascript.
The app was developped inside docker containers and uses Travis CI to run tests when new commits are being made.

It uses a free Alphavantage API key so it is only for demo purpose due to the limited number of requests allowed by the API. For a normal use the free account would need to be upgraded to premium

To run the app run: docker-compose up and go to the indicated address
It comes with an already created Superuser:
    Login: Admin
    Pwd: Peanut1234

Contents:

Dockerfile and docker-compose.yml are used to setup the containerised docker environment

.travis.yml contains the info required by Travis to build and test the app when it detects new commits

stocks_tracks/settings contains all the settings for the app and database

/stocks contains the acutal app:
    -static contains CSS and Javascript files to style the app and manage some functionalities like Ajax requests
    -templates contains all the html files and templates to be rendered by the app
    -models.py contains all the info to create the database
    -admin.py links database elements to the admin website
    -tests.py contains all the tests
    -urls.py contains all the routing for the app
    -views.py contains all the modules

