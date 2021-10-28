from application_services.imdb_artists_resource import IMDBArtistResource
from application_services.UsersResource.user_service import UserResource, AddressResource
from application_services.imdb_users_resource import IMDBUserResource
from database_services.RDBService import RDBService as RDBService

from flask import Flask, redirect, url_for, request, render_template, Response
from flask_dance.contrib.google import make_google_blueprint, google
from flask_cors import CORS
import json, os
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)
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

@app.route("/", methods = ['GET'])
def hi():
    return "Hello, World!"

@app.route("/index", methods = ['GET'])
def index():
    if not google.authorized:
        return redirect(url_for("google.login"))
    google_data = google.get('/oauth2/v2/userinfo')
    assert google_data.ok, google_data.text
    # print(json.dumps(google_data, indent=2))
    # return "You are {email} on Google".format(email=google_data.json()["email"])
    #res = UserResource.get_by_template({"email":google_data.json()["email"]}) # return list of dict
    res = UserResource.get_by_template({"email":google_data.json()["email"]}) # return list of dict
    if len(res) == 0:
        rsp = Response(json.dumps({
            "firstName": google_data.json()["given_name"],
            "lastName": google_data.json()["family_name"],
            "email":google_data.json()["email"] 
            }, default=str), status=200, content_type="application/json")
    else:
        rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp
    # return render_template("index.html", email=google_data.json()["email"])



@app.route('/api/users', methods = ['GET'])
def get_users():
    if request.args.get('limit'):
        limit = request.args.get('limit')
    else:
        limit = "10"
    if request.args.get('offset'):
        offset = request.args.get('offset')
    else:
        offset = "0"
    
    res = UserResource.get_by_template(None, limit, offset)
    for item in res:
        item["links"] = [
            {"rel": "self", "href": f"/api/users/{item['id']}"},
            {"rel": "address", "href":f"/api/address/{item['address_id']}"}
        ]
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/api/users/<prefix>', methods = ['GET'])
def get_users_resource(prefix):
    res = UserResource.get_by_template({"id": prefix})
    res[0]["links"] = [
            {"rel": "self", "href": f"/api/users/{res[0]['id']}"},
            {"rel": "address", "href":f"/api/address/{res[0]['address_id']}"}
    ]
    rsp = Response(json.dumps(res[0], default=str), status=200, content_type="application/json")
    return rsp

@app.route('/api/address/<prefix>', methods = ['GET'])
def get_address_resource(prefix):
    res = AddressResource.get_by_template({"address_id": prefix})
    rsp = Response(json.dumps(res, default=str), status=200, content_type="application/json")
    return rsp

@app.route('/api/create', methods = ['POST'])
def create_user():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    email = request.form.get('email')
    address = request.form.get('address')
    zip_code = request.form.get('zip')
    next_id = int(UserResource.get_next_id("id")[0]["max_id"]) + 1
    next_address_id = int(AddressResource.get_next_id("address_id")[0]["max_id"]) + 1

    AddressResource.create_data_resource({
        "address_id": next_address_id,
        "address": address,
        "zip": zip_code
        })
    
    UserResource.create_data_resource({
        "firstName": firstName,
        "lastName": lastName,
        "email": email,
        "id": next_id,
        "address_id": next_address_id
        })
    
    return f"{firstName} are now a user! Checkout /api/users/{next_id}"

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
