# Course-update-for-Heroku

This is a website that I designed using Flask to work both locally as well as able to be deployed on heroku. The website has many useful features such as redis workers for background tasks, a database attached to it to store information, connected to AWS's S3 storage service, and many more.
The website allows users to create their own profiles and store their password safely in the database with encryption. From there the user can enter some basic information to track tailored updates on other websites and receive notification via both email and a discord bot. The user also has an option to automate the scraping of contents on "canvas" a platform used by the university to deliver course cotent.

## Getting Started

pip install the requirements.txt

set Flask_App = server.py

*Set up tokens for emails, discord bot, s3 bots

Flask Run

### Prerequisites

*If you intend to host the website locally read the following

Install Redis, Execute Redis-Cli, Execute Redis-server (Linux enviroment is recommended as redis does not run very well in Windows)

*If you intent to host this on Heroku read the following

Attach Heroku-Redis to your Heroku app

Attach Heroku SQL to your app


## Deployment

The enviroment variables are set up in a way such that this can be directed ported to heroku with the current procfile with minimal configuration (adding tokens to enviroment on Heroku)


## Authors

* **Wilson Tu** - *Initial work* - [Tu1026](https://github.com/Tu1026)

## Acknowledgments
* Credits to Miguel Grinberg and the Flask Mega Tutorial written by him as the main design philosophy and my understanding of flask came from the detailed explanation in the tutorial.  
