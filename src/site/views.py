from datetime import datetime
from flask import render_template, session, redirect, url_for
from .forms import siteForm, searchForm
from ..models import Site, SearchWord
from . import site
from .. import db


@site.route("/sites", methods=['GET', 'POST'])
def nav_site():
    form = siteForm()
    search_form = searchForm()
    sites = Site.query.order_by(Site.number.desc()).all()
    if form.validate_on_submit():
        exit_title = Site.query.filter_by(title=form.title.data).all()
        exit_body = Site.query.filter_by(title=form.body.data).all()
        if exit_title or exit_body:
            return
        else:
            new_site = Site(title=form.title.data,
                        body=form.body.data,
                        timestamp=datetime.utcnow(),
                        number=0)
            db.session.add(new_site)
        return redirect(url_for(".nav_site"))
    if search_form.validate_on_submit():
        word = SearchWord.query.filter_by(body=search_form.body.data).first()
        if word:
            word.number +=1
        else:
            word = SearchWord(body=form.body.data,
                              number=1)
            db.session.add(word)
        return redirect('https://www.google.com/#q='+ word.body)
    return render_template('website.html', form=form, search_form=search_form, sites=sites)


@site.route('/add-clicks/<int:id>')
def add_click(id):
    site = Site.query.get_or_404(id)
    site.number += 1
    db.session.add(site)
    return redirect(site.body)