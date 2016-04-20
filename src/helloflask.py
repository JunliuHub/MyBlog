import os
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from flask import Flask, render_template, session, redirect, url_for
from datetime import datetime

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'IT IS A BUG'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)


class NameForm(Form):
    name = StringField("what is your name?", validators=[InputRequired()])
    submit = SubmitField('submit')


class NewBlogForm(Form):
    title = StringField('标题', validators=[InputRequired()])
    body = TextAreaField('写点儿什么', validators=[InputRequired()])
    submit = SubmitField('发表新文章')


class Blog(db.Model):
    __talbename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return '<Blog %s>' %self.title


@app.route('/', methods=['GET', 'POST'])
def index():
    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
    return render_template('index.html', blogs=blogs, current_time=datetime.utcnow(),
                           name=session.get('name'), text=session.get('text'))


@app.route('/blogs/new', methods=['GET', 'POST'])
def new_blog():
    blogform = NewBlogForm()
    if blogform.validate_on_submit():
        blog = Blog(title=blogform.title.data,
                    body=blogform.body.data,
                    timestamp = datetime.utcnow()
                    )
        db.session.add(blog)

        session['name'] = blogform.title.data
        session['text'] = blogform.body.data
        return redirect(url_for('index'))
    return render_template('newblog.html', blogform=blogform, current_time=datetime.utcnow())


@app.route('/blogs/<int:id>')
def blog(id):
    blog = Blog.query.get_or_404(id)
    return render_template('blog.html', blog=blog)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
