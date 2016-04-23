from flask.ext.pagedown.fields import PageDownField
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired
from flask.ext.wtf import Form


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


class EditContentForm(Form):
    body = PageDownField('修改笔记？', validators=[InputRequired()])
    submit = SubmitField('保存修改')