from urllib import request

from flask import Flask, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.title

# One time to create db
# with app.app_context():
#     db.create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create-article/', methods=['GET', 'POST'])
def create_article():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        article = Article(title=title, content=content)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return "Error while adding article" + str(e)
    else:
        return render_template('create-article.html')


@app.route('/posts/')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template('posts.html', articles=articles)


@app.route('/posts/<int:post_id>/delete/')
def delete_article(post_id):
    article = Article.query.get_or_404(post_id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect(url_for('posts'))
    except Exception as e:
        return "Error while deleting article" + str(e)


@app.route('/posts/<int:post_id>/edit/', methods=['GET', 'POST'])
def edit_article(post_id):
    article = Article.query.get(post_id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']



        try:
            db.session.commit()
            return redirect(url_for('posts'))
        except Exception as e:
            return "Error while editing article" + str(e)
    else:

        article = Article.query.get(post_id)
        return render_template('post_edit.html', article=article)


@app.route('/posts/<int:post_id>/')
def post_details(post_id):
    article = Article.query.get(post_id)
    return render_template('post_details.html', article=article)


@app.route('/about/')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
