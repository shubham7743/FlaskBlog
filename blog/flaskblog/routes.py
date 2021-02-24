#contains all the routes/ url path used in website
import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Post, UpVote
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from sqlalchemy import func


@app.route("/")
@app.route("/home")
@app.route("/home/<int:filter>")
def home(filter = 1):
    db.create_all()
    page = request.args.get(str(filter) + 'page', 1, type=int)
    if( filter == 1):
        posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    elif( filter == 2):
        posts = Post.query.order_by(Post.date_posted.asc()).paginate(page=page, per_page=5)
    elif(filter == 3):
        posts = db.session.query(Post).join(UpVote).group_by(Post.id).order_by(func.count().desc()).paginate(page=page, per_page=5)
    
    #if user is logged in he must have right to like post
    if current_user.is_authenticated:
        return render_template('home.html', posts=posts, upvote = get_current_user_like(), likelist = get_total_post_like())
    #if user is logged out he can only see total likes 
    else:
        return render_template('index.html' , posts = posts , likelist = get_total_post_like())




#about page 
@app.route("/about")
def about():
    return render_template('about.html', title='About')


#to register new user
@app.route("/register", methods=['GET', 'POST'])
def register():
    #if user is already registerd and logged in
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # to generate encrpyeted password using bcrpty
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


#login to uesr account
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#using flask login module to logout user
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


#function to save picture in diffrent name as user upload it to avoid same name exceptions
#random secret token/name is genrated and saved in profile_pics folder
#also reszing of image is done in 125px * 125px so that it load faster  
def save_picture(form_picture): 
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


#page create to update account details and upload profile pics
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


#to upload new post 
@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


#render to update and delete post page  
@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


#to update post
@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


#to delete form
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


# to display all the user post of anyuser user click on post link
@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


# mail send to reset password
# possible that it may go in spam folder
def send_reset_email(user):
    # to check authentication of user
    token = user.get_reset_token()
    #message that will contain link to change password 
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


#this page will take request to change password and send mail to user mail with link to change password
@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


#update new password of user 
@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)


#get likes of current user/active account user
def get_current_user_like():
    upvote = UpVote.query.all()
    likelist = []
    for vote in upvote:
        if(vote.user_id == current_user.id):
            likelist.append(vote.post_id)
    return likelist

#user to upvote on post
@app.route("/like_post/<int:post_id>/<int:user_id>", methods=['GET', 'POST'])
@login_required
def like_post(post_id,user_id):
    flag = 0
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)

    check = UpVote.query.all()
    for vote in check:
        if(vote.user_id == user_id and vote.post_id == post_id):
            flag = 1
            break
    if(flag == 0):
        upvote = UpVote(user_id = user_id , post_id = post_id)
        db.session.add(upvote)
        db.session.commit() 
    return render_template("home.html" ,posts = posts, upvote = get_current_user_like() ,  likelist = get_total_post_like()) 


#get total likes on individual post
def get_total_post_like():
    upvote = UpVote.query.all()
    posts = Post.query.order_by(Post.date_posted.desc()).first()
    if posts:
        likelist = [0] * posts.id    
        i = 1
        for vote in upvote:
            likelist[vote.post_id -1] += 1
    else:
        likelist = []
    return(likelist)