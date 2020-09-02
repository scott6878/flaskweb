from flask import Flask, g, request, Response, make_response
from flask import session, render_template, Markup, url_for
from datetime import date, datetime, timedelta
import os
from helloflask.init_db import init_database, db_session

app = Flask(__name__)
import helloflask.views
import helloflask.tests
import helloflask.filters

app.debug = True
app.jinja_env.trim_blocks = True

# config["connect_args"] = {"options": "-c timezone=utc"}

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

app.config.update(
    connect_args={"options": "-c timezone=utc"},
	SECRET_KEY='X1243yRH!mMwf',
	SESSION_COOKIE_NAME='pyweb_flask_session',
	PERMANENT_SESSION_LIFETIME=timedelta(31)      # 31 days
)

@app.before_first_request
def beforeFirstRequest():
    print(">> before_first_request!!")
    init_database()   # initialize database 


@app.after_request
def afterReq(response):
    print(">> after_request!!")
    return response


@app.teardown_request
def teardown_request(exception):
    print(">>> teardown request!!", exception)


@app.teardown_appcontext
def teardown_context(exception):
    print(">>> teardown context!!", exception)
    db_session.remove()   # remove used db-session


