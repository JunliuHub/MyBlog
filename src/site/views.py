from datetime import datetime
from flask import render_template, session, redirect, url_for
from .forms import siteForm
from ..models import Site
from . import site
from .. import db


@site.route("/sites", methods=['GET', 'POST'])
def nav_site():
    form = siteForm()
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
    return render_template('website.html', form=form, sites=sites)


@site.route('/add-clicks/<int:id>')
def add_click(id):
    site = Site.query.get_or_404(id)
    site.number += 1
    db.session.add(site)
    return redirect(site.body)