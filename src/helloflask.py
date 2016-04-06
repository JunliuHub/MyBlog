from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired
from flask import Flask, render_template, session, redirect, url_for, flash
from datetime import datetime


app = Flask(__name__)
bootstrap = Bootstrap(app)
moment = Moment(app)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'IT IS A BUG'


class NameForm(Form):
    name = StringField("what is your name?", validators=[InputRequired()])
    submit = SubmitField('submit')


class NewBlogForm(Form):
    name = StringField('标题', validators=[InputRequired()])
    text = TextAreaField('写点儿什么', validators=[InputRequired()])
    submit = SubmitField('发表新文章')



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', current_time=datetime.utcnow(),
                           name=session.get('name'), text=session.get('text'))


@app.route('/blogs/new', methods=['GET', 'POST'])
def new_blog():
    blogform = NewBlogForm()
    if blogform.validate_on_submit():
        session['name'] = blogform.name.data
        session['text'] = blogform.text.data
        return redirect(url_for('index'))
    return render_template('newblog.html', blogform=blogform, current_time=datetime.utcnow())



@app.errorhandler(404)
def page_not_found():
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
