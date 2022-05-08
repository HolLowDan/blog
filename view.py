from flask import render_template, redirect, request
from flask_security import login_required

from app import app, db
from loginform import LoginForm
from model import Article


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def posts_detail(id):
    article = Article.query.get(id)
    return render_template("posts_detail.html", article=article)


@login_required
@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Ошибка при удалении"


@login_required
@app.route('/posts/<int:id>/update', methods=['POST', "GET"])
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании статьи произошла ошибка'
    else:
        return render_template("post_update.html", article=article)


@login_required
@app.route('/create_article', methods=['POST', "GET"])
def create_article():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template("create_article.html")


@app.route('/login_user', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login_user.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.errorhandler(404)
def error_404(e):
    return render_template('404.html'), 404
