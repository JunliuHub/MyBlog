from datetime import datetime
from flask import render_template, session, redirect, url_for

from . import main
from .forms import NewBlogForm, EditContentForm, EditBlogForm, ContentForm
from .. import db
from ..models import Blog, BlogContent


@main.route('/', methods=['GET', 'POST'])
def index():
    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
    return render_template('index.html', blogs=blogs, current_time=datetime.utcnow(),
                           name=session.get('name'), text=session.get('text'))


@main.route('/blogs/new', methods=['GET', 'POST'])
def new_blog():
    blogform = NewBlogForm()
    if blogform.validate_on_submit():
        blog = Blog(title=blogform.title.data,
                    body=blogform.body.data,
                    timestamp=datetime.utcnow()
                    )
        db.session.add(blog)
        return redirect(url_for('.index'))
    return render_template('newblog.html', blogform=blogform, current_time=datetime.utcnow())


@main.route('/blogs/<int:id>', methods=['GET', 'POST'])
def blog(id):
    content_form = ContentForm()
    blog = Blog.query.get_or_404(id)
    session['id'] = blog.id
    if content_form.validate_on_submit():
        new_content = BlogContent(body=content_form.body.data,
                                  blog=blog,
                                  timestamp=datetime.utcnow())
        db.session.add(new_content)
        return redirect(url_for('.blog', id=blog.id))
    return render_template('blog.html', blog=blog, content_form=content_form)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_blog(id):
    blog = Blog.query.get_or_404(id)
    form = EditBlogForm()
    if form.validate_on_submit():
        blog.title = form.title.data
        blog.body = form.body.data
        return redirect(url_for('.blog', id=blog.id))
    form.title.data = blog.title
    form.body.data = blog.body
    return render_template('edit_blog.html', blog=blog, form=form)


@main.route('/edit/contents/<int:id>', methods=['GET', 'POST'])
def edit_content(id):
    content = BlogContent.query.get_or_404(id)
    form = EditContentForm()
    if form.validate_on_submit():
        content.body = form.body.data
        return redirect(url_for('.blog', id=session.get('id')))
    form.body.data = content.body
    return render_template('edit_blog.html', content=content, form=form)


@main.route('/delete/content/<int:id>')
def delete_content(id):
    content = BlogContent.query.get_or_404(id)
    db.session.delete(content)

    return redirect(url_for('.blog', id=session.get('id')))


@main.route('/delete/blog/<int:id>')
def delete_blog(id):
    blog = Blog.query.get_or_404(id)
    db.session.delete(blog)

    return redirect(url_for('.index'))