import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flasky.models import User, Post
from flasky.forms import registration_form, login_form, update_account_form, post_form
from flasky import app, db, bcrypt
from datetime import date

posts = []

# Home Page
@app.route('/')
@app.route('/home')
def home():
    # Display all posts
    posts = Post.query.all()
    return render_template('home.html', posts=posts, date=date.today().strftime('%Y-%m-%d'))

# About Page
@app.route('/about')
def about():
    return render_template('about.html', title='About', date=date.today().strftime('%Y-%m-%d'))


# Registration
@app.route('/register', methods=['GET','POST'])
def register():
    # If navigated to while already logged in
    if(current_user.is_authenticated):
        return redirect(url_for('home'))

    # Get user information and log to db
    form = registration_form()
    if(form.validate_on_submit()):
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data,email=form.email.data,password=hashed_pass,admin = form.username.data == 'SegwayBillson')
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}! You can now login!', 'success')
        # Have the new user log in
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form, date=date.today().strftime('%Y-%m-%d'))


# Login
@app.route('/login', methods=['GET','POST'])
def login():
    # If navigated to while already logged in
    if(current_user.is_authenticated):
        return redirect(url_for('home'))

    # Get user log in info
    form = login_form()
    if(form.validate_on_submit()):
        user = User.query.filter_by(email=form.email.data).first()
        if(user and bcrypt.check_password_hash(user.password, form.password.data)):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email/password.', 'danger')

    return render_template('login.html', title='Login', form=form, date=date.today().strftime('%Y-%m-%d'))


# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Code for resizing, renaming, and saving new profile picture
def save_pic(form_picture):
    # Generate random image name
    rand_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    pic_name = rand_hex + f_ext
    pic_path = os.path.join(app.root_path,'static/profile_pics',pic_name)
    output_size = (125,125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(pic_path)
    return pic_name

# Account
@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    form = update_account_form()
    if(form.validate_on_submit()):
        # Update picture data if necessary
        if(form.picture.data):
            pic_file = save_pic(form.picture.data)
            current_user.image = pic_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account updated!', 'success')
        return redirect(url_for('account'))

    # Populate fields with current data
    elif(request.method == 'GET'):
        form.username.data = current_user.username
        form.email.data = current_user.email

    image = url_for('static', filename='profile_pics/' + current_user.image)
    return render_template('account.html', title='Account', image=image, form=form, date=date.today().strftime('%Y-%m-%d'))

# Create Post
@app.route('/post/new', methods=['GET','POST'])
@login_required
def new_post():
    form = post_form()
    if(form.validate_on_submit()):
        post = Post(title=form.title.data,content=form.content.data, author=current_user, announce= request.form.get('announce') == 'checked')
        db.session.add(post)
        db.session.commit()
        flash('Post Submitted!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',form=form, legend='New Post', date=date.today().strftime('%Y-%m-%d'))

# About Page
@app.route('/administration')
@login_required
def admin():
    if(current_user.admin):
        return render_template('administration.html', title='Administration', users=User.query.all(), date=date.today().strftime('%Y-%m-%d'))
    return redirect(url_for('home'))

# Post Page
@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post, date=date.today().strftime('%Y-%m-%d'))

# Update Page
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = post_form()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post', date=date.today().strftime('%Y-%m-%d'))


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


# Announcement Page
@app.route('/')
@app.route('/announcements')
def announcements():
    posts = Post.query.filter_by(announce=True)
    return render_template('home.html', posts=posts, date=date.today().strftime('%Y-%m-%d'))
