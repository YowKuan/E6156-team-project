from flask import Flask, redirect, url_for, request
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS
import json, os
import logging

app = Flask(__name__)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

client_id = "126427133643-l3o225t3jkjie0rfud0971i29p4peeqn.apps.googleusercontent.com"
client_secret = "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"
app.secret_key = "supersekrit"
blueprint = make_google_blueprint(
    client_id=client_id,
    client_secret=client_secret,
    scope=["profile", "email"]
)
app.register_blueprint(blueprint, url_prefix="/login")

@app.route("/")
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get('/oauth2/v2/userinfo')
    assert resp.ok, resp.text
    print(f"==========")
    print(resp.json(), resp.ok, resp.text)
    return "You are {email} on Google".format(email=resp.json()["email"])

if __name__ == "__main__":
    #app.run(ssl_context='adhoc')
    app.run()