from flask import Flask, g
app = Flask(__name__)
app.debug = True


@app.before_request
def before_request():
    print("before_request!!!")
    g.str = "한글"

@app.route("/")
def helloworld():
    return "hello Flask World!" + getattr(g, 'str', '111')
 

#../start_flask.py
