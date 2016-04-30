from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired,URL
from flask.ext.wtf import Form

class siteForm(Form):
    title = StringField("名称", validators=[InputRequired()])
    body = StringField("网址", validators=[URL()])
    submit = SubmitField("添加")
