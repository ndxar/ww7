from flask import Blueprint, render_template, request, flash, redirect, url_for, get_flashed_messages
from flask_login import login_required, current_user
from .models import Post, User
from . import db
import markdown
from sqlalchemy import desc
from markupsafe import Markup
from jinja2 import Template
from werkzeug.security import generate_password_hash, check_password_hash

views = Blueprint('views', __name__)

parser = markdown.Markdown(extensions = ['meta'])                                           #MD PARSER

@views.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', user=current_user,posts=posts)

@views.route('/post', methods=['GET','POST'])
@login_required
def post():
    if request.method == "POST":
        content = request.form.get('content')
        parser.convert(content)
        meta = parser.Meta
        if not content:
            flash('Post no puede estar vacio', category='error')
        elif meta.get("url") is None or meta.get("url")[0] == '':
            flash('Url no puede estar vacia', category='error')
        elif meta.get("title") is None or meta.get("title")[0] == '':
            flash('Title no puede estar vacio', category='error')
        else:   
            post = Post(content=content, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Posteado :-)')

        return render_template('create_post.html', user = current_user, content=content)

    return render_template('create_post.html', user = current_user)



@views.route('/~<username>')
def userpage(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No hay autor con ese usuario', category='error')
        return redirect(url_for('views.home'))
    
    #posts = user.posts no usado para usar el order_by
    posts = Post.query.filter_by(author=user.id).order_by(Post.creationDate.desc()).all()
    db.session.flush()

    entries = []
    for post in posts:
        #post.content = {"html": parser.convert(post.content) , "meta":parser.Meta}
        post.content = parser.convert(post.content)
        entry= [post, parser.Meta]
        entries.append(entry)

    theme = Template(user.userTheme)

    return render_template(theme, posts=entries)



@views.route('/~<username>/<url>')
def postpage(username,url):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash('No hay autor con ese usuario', category='error')
        return redirect(url_for('views.home'))

    posts = user.posts

    for post in posts:
        #post.content = {"html": parser.convert(post.content) , "meta":parser.Meta}
        post.content = Markup(parser.convert(post.content))
        meta = parser.Meta

        if (parser.Meta.get('url') is not None) and (str(parser.Meta['url'][0]) == url):
            #reqPost = post
            reqPost = post
            reqMeta = meta
            break
        elif str(post.id) == url:
            #reqPost = post
            reqPost = post
            reqMeta = meta
            break
    
    try:
        reqPost
    except:
        flash('No hay posts de ese usuario con esa URL', category='error')
        return redirect(url_for('views.home'))

    theme = Template(user.postTheme)

    return render_template(theme, post=reqPost, meta=reqMeta)


@views.route('/theme', methods=['GET','POST'])
@login_required
def theme():
    if request.method == "POST":
        userTheme = request.form.get('userTheme')
        postTheme = request.form.get('postTheme')

        current_user.userTheme = userTheme
        current_user.postTheme = postTheme
        db.session.commit()
        flash('Updated theme :D')

    return render_template("theme.html", user=current_user)

@views.route('/settings', methods=['GET','POST'])
@login_required
def settings():
    if request.method == "POST":
        in_email = request.form.get('email')
        in_username = request.form.get('username')
        in_password = request.form.get('password')

        if check_password_hash(current_user.passwordHash, in_password):
            if in_email != current_user.email:
                email_existe = User.query.filter_by(email=in_email).first()
                if email_existe:
                    flash("email already in use", category="error")
                else:
                    current_user.email = in_email
                    flash("email changed!",category="success")
            
            if in_username != current_user.username:
                user_existe = User.query.filter_by(username=in_username).first()
                if user_existe:
                    flash("username already in use",category="error")
                else:
                    current_user.username = in_username
                    flash("username changed!",category="success")
            db.session.commit()
        else:
            flash("incorrect password",category="error")

    return render_template("settings.html", user=current_user)