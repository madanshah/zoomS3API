from flask import Flask, session, redirect, request, jsonify, render_template, url_for, make_response, flash
from flask_awscognito import AWSCognitoAuthentication
import requests
import json
from flask_awscognito import AWSCognitoAuthentication
from flask_cors import CORS
from jwt.exceptions import InvalidKeyError
from flask_jwt_extended import (
    JWTManager,
    set_access_cookies,
    verify_jwt_in_request_optional,
    get_jwt_identity,
)
import os
import boto3

import datetime
from datetime import date, timedelta

# from keys import get_cognito_public_keys
app = Flask(__name__)
app.secret_key = b'\x03\x94Hw#G\xbc\x11;\x86\xa0O\xa0\xf1x6'
app.config['AWS_DEFAULT_REGION'] = 'ap-south-1'
app.config['AWS_COGNITO_DOMAIN'] = 'https://zoomgen.auth.ap-south-1.amazoncognito.com'
app.config['AWS_COGNITO_USER_POOL_ID'] = 'ap-south-1_e1X5i4bar'
app.config['AWS_COGNITO_USER_POOL_CLIENT_ID'] = '1q9hccr3c083h6esv648u3mt4c'
app.config['AWS_COGNITO_USER_POOL_CLIENT_SECRET'] = '1ht0lfhnkaghgv7atm4q8vlkasb181rr3lu57p3si00hb287d3jo'
app.config['AWS_COGNITO_REDIRECT_URL'] = 'https://zenum.genesesolution.com/dash'
# app.config.from_object("config")
# app.config["JWT_PUBLIC_KEY"] = RSAAlgorithm.from_jwk(get_cognito_public_keys())

dynamodb = boto3.resource('dynamodb',
             aws_access_key_id=os.environ["ACCESS_KEY_ID"],
             aws_secret_access_key =os.environ["ACCESS_SECRET_KEY"],
             region_name=os.environ["AWS_REGION"])

from boto3.dynamodb.conditions import Key, Attr

headers = {
    'content-type': "application/json",
    # For main account
    # 'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2Mzk3MjM1NjAsImlhdCI6MTYwNzU4MjgxNn0.zf0B_XNGKlPxcll02w85T9P-s94PQb-1JLSfStHZRI4"
    # Babin accounts
    'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IjNDNkdpNmtiUnpXS1NMZktVMU56RXciLCJleHAiOjE2NDE4Mzg1MDAsImlhdCI6MTYxMDM0NTgxN30.RXOymitbE09WJiAN9JXZevMLysHjVc53jysCfv4iLwA"

}
# @app.route("/index")
# def index():
#     return render_template("dashboard.html")
CORS(app)
aws_auth = AWSCognitoAuthentication(app)
jwt = JWTManager(app)

@app.route("/")
def index():
    # url = "https://api.zoom.us/v2/users"
    # querystring = {"page_size":"100","status":"active"}
    # response = requests.get(url, headers=headers, params=querystring)
    # df = json.loads(response.content)
    # us = df['users']
    if 'uname' in session:
        user = session['uname']
        return render_template("dash101.html", user=user)    
    return render_template("dash102.html")
    

# @app.route("/dash")
# def dash():
#     return render_template("dash101.html")    

@app.route("/login", methods=["POST"])
def login():
    # return redirect(aws_auth.get_sign_in_url())
        return render_template("login.html")    
    
@app.route("/check", methods=["POST"])
def check():
    email = request.form['email']
    # userName = request.form['userName']
    password = request.form['password']

    table = dynamodb.Table('zoomUser')
    response = table.query(KeyConditionExpression=Key('email').eq(email))
    print(response)
    if response['Count'] == 1:
        items = response['Items']
        # print(items)

        name = items[0]['userName']
        session['uname'] = name
        if password == items[0]['password']:
            return render_template("dash101.html", name=name)
        flash("incorrect user or password","warning")
        return render_template("login.html")
    else:
        flash("incorrect user or password","warning")
        return render_template("login.html")

# @app.route("/loggedin", methods=["GET"])
# def logged_in():
#     access_token = aws_auth.get_access_token(request.args)
#     resp = make_response(redirect(url_for("protected")))
#     set_access_cookies(resp, access_token, max_age=30 * 60)
#     print(resp)
#     return resp

# @app.route("/secret")
# def protected():
#     verify_jwt_in_request_optional()
#     if get_jwt_identity():
#         return render_template("dash101.html")
#     else:
#         return redirect(aws_auth.get_sign_in_url())


@app.route("/userlist",methods=['POST'])
def userlist():
    url = "https://api.zoom.us/v2/users"
    querystring = {"page_size":"100","status":"active"}
    response = requests.get(url, headers=headers, params=querystring)
    df = json.loads(response.content)
    print(response.content)
    print(type(df))
    print(df)
    us=df
    print(type(us))
    return render_template("userlist.html", us=us)


@app.route("/usercreate",methods=['POST'])
def userCreate():
    return render_template("usercreate.html",)

@app.route("/create",methods=['POST'])
def Create():
    # sa = request.form['subAccount']
    # if sa == "1":
    #     headers = {
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"

    #     }
    # # elif sa == "2":
    # #     headers = {
    # #         'content-type': "application/json",
    # #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2MDg4ODk1MjcsImlhdCI6MTYwODI4NDcyNn0.pppNJoLZOGH7bZf8CLezPDkpzOTZM38-MieXTf3e83g"

    # #     }
    # else:
    #     headers = {
    #         'content-type': "application/json",
    #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODMxNDAsImlhdCI6MTYwOTE0MTg2NX0.iJ7MUvwBVv_5ACHOddTDFFmHJ00A3le968k14rXIjwE"

    #     }
    # # else:
    # #     headers={
    # #         'content-type': "application/json",
    # #         'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOm51bGwsImlzcyI6IngzY2U5OTF4VERtNWZlazZ6dWIxdVEiLCJleHAiOjE2NDA2ODM0NDAsImlhdCI6MTYwOTE0MjA1NX0.Ya_nthCN1sN7RvxRT1VH0sf6GpkxNQux6sYkYA-NWYM"
    # #     }        
    email = request.form['email']
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    type = request.form['licenseType']
    license = "2"
    issuedby = session['uname']
    duration = (request.form['duration'])
    if duration == "365":
        add = 365
    else:
        add=30
    url = "https://api.zoom.us/v2/users"
    payload = "{\"action\":\"create\",\"user_info\":{\"email\":\""+email+"\",\"type\":\""+license+"\",\"first_name\":\""+firstName+"\",\"last_name\":\""+lastName+"\"}}"
    # # jpayload = json.dumps(payload)
    response = requests.post(url, data=payload, headers=headers)
    data = json.loads(response.content)
    print(data)
    print(data['id'])
    table = dynamodb.Table('zoom')
    table.put_item(
        Item={
            'ZoomUser_Email': email,
            'Issued_Date' : date.today().isoformat(),
            'Duration' : duration,
            'Expiry_Date' : (date.today() + datetime.timedelta(days=add)).isoformat(),
            'Issued_By' : issuedby,
            'Participants' : type,
            'ZoomID' : data['id'],
            'SubAccount' : 'Zoom1'
        }
    )

    msg = "Record created"

    return render_template("create.html", data=data, msg=msg)
    # return render_template("create.html", email=email, url=url,type=type, firstName=firstName, lastName=lastName)

@app.route("/userdetail",methods=['POST'])
def userdetail():
    id = request.form['id']
    url = "https://api.zoom.us/v2/users/{}".format(id)
    querystring = {"page_size":"30","status":"active"}
    response = requests.get(url, headers=headers, params=querystring)
    userdetail = response.content
    return render_template("userdetail.html", userdetail=userdetail)

@app.route("/userdelete",methods=['POST'])
def userdelete():
    id = request.form['id']
    url = "https://api.zoom.us/v2/users/{}".format(id)
    querystring = {"action":"disassociate"}
    response = requests.delete(url, headers=headers, params=querystring)
    userinfo = response.content
    return render_template("userdetail.html", userinfo=userinfo)

@app.route("/logout", methods=["POST"])
def logout():
    session.pop('uname', None)
    msg = "you have logged out"
    return render_template("dash102.html", msg=msg)

if __name__ =="__main__":	
    app.run(host='0.0.0.0')




