import os
import bleach
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.pagedown import PageDown
from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask import Flask, render_template, session, redirect, url_for
from datetime import datetime
from markdown import markdown

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
pagedown = PageDown(app)


class NewBlogForm(Form):
    title = StringField('标题', validators=[InputRequired()])
    body = PageDownField('写点儿什么', validators=[InputRequired()])
    submit = SubmitField('发表新文章')


class EditBlogForm(Form):
    title = StringField('标题', validators=[InputRequired()])
    body = PageDownField('写点儿什么', validators=[InputRequired()])
    submit = SubmitField('保存修改')


class ContentForm(Form):
    body = PageDownField('添加点笔记？', validators=[InputRequired()])
    submit = SubmitField('添加新内容')


class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    contents = db.relationship('BlogContent', backref='blog')

    def __repr__(self):
        return '<Blog %s>' % self.title

    @staticmethod
    def on_changed_body(target, body, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i',
                        'li', 'ol', 'pre', 'strong', 'ul', 'h1', 'h2', 'h3', 'p']
        body_html = markdown(body, output_format='html')
        cleaned_body_html = bleach.clean(body_html, tags=allowed_tags, strip=True)
        target.body_html = bleach.linkify(cleaned_body_html)


class BlogContent(db.Model):
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))



    def __repr__(self):
        return '<Belong to %s>' % self.blog.title


db.event.listen(Blog.body, 'set', Blog.on_changed_body)
db.event.listen(BlogContent.body, 'set', Blog.on_changed_body)


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
                    timestamp=datetime.utcnow()
                    )
        db.session.add(blog)
        return redirect(url_for('index'))
    return render_template('newblog.html', blogform=blogform, current_time=datetime.utcnow())


@app.route('/blogs/<int:id>', methods=['GET', 'POST'])
def blog(id):
    content_form = ContentForm()
    blog = Blog.query.get_or_404(id)
    if content_form.validate_on_submit():
        new_content = BlogContent(body=content_form.body.data,
                                  blog=blog,
                                  timestamp=datetime.utcnow())
        db.session.add(new_content)
        return redirect(url_for('blog', id=blog.id))
    return render_template('blog.html', blog=blog, content_form=content_form)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    form = EditBlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.body = form.body.data
        return redirect(url_for('blog', id=blog.id))
    form.title.data = blog.title
    form.body.data = blog.body
    return render_template('edit_blog.html', blog=blog, form=form)


@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
