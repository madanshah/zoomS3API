from flask import Flask, redirect, request, jsonify, render_template, url_for, make_response
from flask_awscognito import AWSCognitoAuthentication
import requests
import json
from flask_awscognito import AWSCognitoAuthentication
from flask_cors import CORS
from jwt.algorithms import RSAAlgorithm
from jwt.exceptions import InvalidKeyError
from flask_jwt_extended import (
    JWTManager,
    set_access_cookies,
    verify_jwt_in_request_optional,
    get_jwt_identity,
)

from keys import get_cognito_public_keys
app = Flask(__name__)

app.config['AWS_DEFAULT_REGION'] = 'us-east-1'
app.config['AWS_COGNITO_DOMAIN'] = 'https://zooms3.auth.us-east-1.amazoncognito.com'
app.config['AWS_COGNITO_USER_POOL_ID'] = 'us-east-1_jq7p3tyEK'
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '3stdq8ji450g3s02jairo70iub'
app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = 'ik7ri7skh06oi4t2c8ilne82t3ajah40qba9t0127vi48gu894c'
app.config['AWS_COGNITO_REDIRECT_URL'] = 'http://localhost/'
# app.config.from_object("config")
# app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(get_cognito_public_keys())


# headers = {
#     'content-type': "application/json",
#     # For main account
#     # 'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2Mzk3MjM1NjAsImlhdCI6MTYwNzU4MjgxNn0.zf0B_XNGKlPxcll02w85T9P-s94PQb-1JLSfStHZRI4"
#     # Babin accounts
#     'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"

# }
# @app.route("/index")
# def index():
#     return render_template("dashboard.html")
CORS(app)
aws_auth = AWSCognitoAuthentication(app)
jwt = JWTManager(app)

@app.route("/")
def dash():
    # url = "https://api.zoom.us/v2/users"
    # querystring = {"page_size":"100","status":"active"}
    # response = requests.get(url, headers=headers, params=querystring)
    # df = json.loads(response.content)
    # us = df['users']
    return render_template("dash101.html")

@app.route("/login", methods=["POST"])
def login():
    return redirect(aws_auth.get_sign_in_url())
    
@app.route("/loggedin", methods=["GET"])
def logged_in():
    access_token = aws_auth.get_access_token(request.args)
    resp = make_response(redirect(url_for("protected")))
    set_access_cookies(resp, access_token, max_age=30 * 60)
    print(resp)
    return resp

@app.route("/secret")
def protected():
    verify_jwt_in_request_optional()
    if get_jwt_identity():
        return render_template("dash101.html")
    else:
        return redirect(aws_auth.get_sign_in_url())


@app.route("/userlist",methods=['POST'])
def userlist():
    sa = request.form['subAccount']
    if sa == "1":
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"

        }
    # elif sa == "2":
    #     headers = {
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2MDg4ODk1MjcsImlhdCI6MTYwODI4NDcyNn0.pppNJoLZOGH7bZf8CLezPDkpzOTZM38-MieXTf3e83g"

    #     }
    else:
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODMxNDAsImlhdCI6MTYwOTE0MTg2NX0.iJ7MUvwBVv_5ACHOddTDFFmHJ00A3le968k14rXIjwE"

        }
    # else:
    #     headers={
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"
    #     }        
    url = "https://api.zoom.us/v2/users"
    querystring = {"page_size":"100","status":"active"}
    response = requests.get(url, headers=headers, params=querystring)
    df = json.loads(response.content)
    # us = df['users']
    us=df
    print(type(us))
    return render_template("testdash.html", us=us)


@app.route("/usercreate",methods=['POST'])
def userCreate():
    return render_template("usercreate.html")

@app.route("/create",methods=['POST'])
def Create():
    sa = request.form['subAccount']
    if sa == "1":
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"

        }
    # elif sa == "2":
    #     headers = {
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2MDg4ODk1MjcsImlhdCI6MTYwODI4NDcyNn0.pppNJoLZOGH7bZf8CLezPDkpzOTZM38-MieXTf3e83g"

    #     }
    else:
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODMxNDAsImlhdCI6MTYwOTE0MTg2NX0.iJ7MUvwBVv_5ACHOddTDFFmHJ00A3le968k14rXIjwE"

        }
    # else:
    #     headers={
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"
    #     }        
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    type = request.form['licenseType']
    url = "https://api.zoom.us/v2/users"
    payload = "{\"action\":\"create\",\"user_info\":{\"email\":\""+email+"\",\"type\":\""+type+"\",\"first_name\":\""+firstName+"\",\"last_name\":\""+lastName+"\"}}"
    # # jpayload = json.dumps(payload)
    response = requests.post(url, data=payload, headers=headers)
    a = response.content
    return render_template("create.html", a=a)
    # return render_template("create.html", email=email, url=url,type=type, firstName=firstName, lastName=lastName)

@app.route("/userdetail",methods=['POST'])
def userdetail():
    sa = request.form['subAccount']
    if sa == "1":
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"

        }
    # elif sa == "2":
    #     headers = {
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2MDg4ODk1MjcsImlhdCI6MTYwODI4NDcyNn0.pppNJoLZOGH7bZf8CLezPDkpzOTZM38-MieXTf3e83g"

    #     }
    else:
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODMxNDAsImlhdCI6MTYwOTE0MTg2NX0.iJ7MUvwBVv_5ACHOddTDFFmHJ00A3le968k14rXIjwE"

        }
    # else:
    #     headers={
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"
    #     }        
    id = request.form['id']
    url = "https://api.zoom.us/v2/users/{}".format(id)
    querystring = {"page_size":"30","status":"active"}
    response = requests.get(url, headers=headers, params=querystring)
    userdetail = response.content
    return render_template("userdetail.html", userdetail=userdetail)

@app.route("/userdelete",methods=['POST'])
def userdelete():
    sa = request.form['subAccount']
    if sa == "1":
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"

        }
    # elif sa == "2":
    #     headers = {
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2MDg4ODk1MjcsImlhdCI6MTYwODI4NDcyNn0.pppNJoLZOGH7bZf8CLezPDkpzOTZM38-MieXTf3e83g"

    #     }
    else:
        headers = {
            'content-type': "application/json",
            'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODMxNDAsImlhdCI6MTYwOTE0MTg2NX0.iJ7MUvwBVv_5ACHOddTDFFmHJ00A3le968k14rXIjwE"

        }
    # else:
    #     headers={
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"
    #     }        
    id = request.form['id']
    url = "https://api.zoom.us/v2/users/{}".format(id)
    querystring = {"action":"disassociate"}
    response = requests.delete(url, headers=headers, params=querystring)
    userinfo = response.content
    return render_template("userdetail.html", userinfo=userinfo)


if __name__ =="__main__":	
    app.run()




