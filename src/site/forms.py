from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired,URL
from flask.ext.wtf import Form


class siteForm(Form):
    title = StringField("名称", validators=[InputRequired()])
    body = StringField("网址", validators=[URL()])
    submit = SubmitField("添加")


class searchForm(Form):
    body = StringField("", validators=[InputRequired()])
    submit = SubmitField("搜索")