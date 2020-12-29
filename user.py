from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, Flask!"

@app.route("/tuna")
def tuna():
    return "<h1>I like Tuna<h1>"

@app.route("/profile/<user>")
def profile(user):
    return "hey there %s, whats up" % user

@app.route("/post/<int:post_id>")
def post(post_id):
    return "<h2>POST Id is %s<h2>" % post_id

if __name__ =="__main__":	
    app.run()



