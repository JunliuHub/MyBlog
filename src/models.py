import bleach
from . import db
from markdown import markdown
from datetime import datetime


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
