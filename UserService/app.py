from flask import Flask, Response, render_template, redirect, url_for
from flask_dance.contrib.google import make_google_blueprint, google
from flask_login import current_user
from flask_cors import CORS
import json, os
import logging

from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource
from application_services.imdb_users_resource import IMDBUserResource
from database_services.RDBService import RDBService as RDBService


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)

client_id = "126427133643-l3o225t3jkjie0rfud0971i29p4peeqn.apps.googleusercontent.com"
client_secret = "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"
app.secret_key = "some secret".encode('utf8') # Used for signature in the future

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    reprompt_consent=True,
    scope=["profile", "email"]
)

app.register_blueprint(blueprint, url_prefix="/login")


@app.route('/')
def index():
    google_data = None
    user_info_endpoint = "/oauth2/v2/userinfo"
    if google.authorized:
        google_data = google.get(user_info_endpoint).json()
        print(json.dumps(google_data, indent=2))
        bp = app.blueprints.get("google")
        s = bp.session
        t = s.token
        print("Token = \n", json.dumps(t, indent=2))
    return render_template("index.j2", google_data=google_data,
                           fetch_url=google.base_url + user_info_endpoint)


@app.route('/imdb/artists/<prefix>')
def get_artists_by_prefix(prefix):
    res = IMDBArtistResource.get_by_name_prefix(prefix)
    rsp = Response(json.dumps(res), status=200, content_type="application/json")
    return rsp


@app.route('/users')
def get_users():
    res = UserResource.get_by_template(None)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/users/<prefix>')
def get_users_resource(prefix):
    res = IMDBUserResource.get_by_name_prefix(prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp


@app.route('/<db_schema>/<table_name>/<column_name>/<prefix>')
def get_by_prefix(db_schema, table_name, column_name, prefix):
    res = RDBService.get_by_prefix(db_schema, table_name, column_name, prefix)
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp




if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
