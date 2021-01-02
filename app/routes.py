from flask import render_template, flash, redirect, url_for, send_file, Response
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from app.models import User, Course
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm, CourseForm, GymForm, ScraperForm, DownloadForm
from app import db, q
from updateScript import main_function
from gymUpdates import update_loop
from canvas_scraper import extraction
import discord
from dotenv import load_dotenv
from pathlib import Path
import shutil
import os
from aws import upload_file, list_files, get_total_bytes, get_object
import boto3
from config import Config


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/help')
def help():
    return render_template('help.html', title='Help')


@app.route('/update', methods=['GET', 'POST'])
@login_required
def update():
    form = CourseForm()
    if form.validate_on_submit():
        q.enqueue(main_function, form.class_name.data, current_user.email, form.url.data, int(form.seats.data))
        flash('Congratulations course has been tracked!')
        return redirect(url_for('index'))
    return render_template('update.html', title='update', form=form)

@app.route('/gym', methods=['GET', 'POST'])
@login_required
def gym():
    form = GymForm()
    if form.validate_on_submit():
        q.enqueue(update_loop, form.class_name.data, form.url.data, current_user.email)
        flash('Congratulations gym has been tracked!')
        return redirect(url_for('index'))
    return render_template('gym.html', title='gym', form=form)

@app.route('/scraper', methods=['GET', 'POST'])
@login_required
def scraper():
    scraper_form = ScraperForm()
    download_form = DownloadForm()
    s3 = get_client()
    if scraper_form.validate_on_submit():
        shutil.rmtree(os.path.join(Config.basedir,'tmp'))
        os.mkdir(os.path.join(Config.basedir,'tmp'))
        q.enqueue(extraction, scraper_form.class_name.data, scraper_form.num.data)
        shutil.make_archive('extraction', 'zip', 'tmp')
        upload_file(s3, 'extraction.zip')
        flash('Downloading and preparing your files hit the download button 5 minutes later')
        # dir_name = Path('/scraper')
        return redirect(url_for('index'))
    if download_form.validate_on_submit():
        total_bytes = get_total_bytes(s3)
        flash('Downloaded')
        # shutil.make_archive('extraction', 'zip', Path('/app'), 'scraper')
        # shutil.make_archive('extraction', 'zip', os.path.join(MYDIR + "/" + "/app"), 'scraper')
        # shutil.move('%s.%s'%('extraction', 'zip'), os.path.join(MYDIR + "/" + "/app"))
        return Response(
        get_object(s3, total_bytes),
        mimetype='text/plain',
        headers={"Content-Disposition": "attachment;filename=extraction.zip"}
    )
    return render_template('scraper.html', title='scraper', form1=scraper_form, form2=download_form)

def get_client():
    load_dotenv()
    AWSUSER_SECRET = os.environ.get('AWSUSER_SECRET')
    AWSUSER_ID = os.environ.get('AWSUSER_ID')
    AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME')
    return boto3.client('s3',
                    'us-west-1',
                    aws_access_key_id= AWSUSER_ID,
                    aws_secret_access_key= AWSUSER_SECRET
                     )
