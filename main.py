from flask import Flask, render_template
import mysql

app = Flask(__name__)
# app.secret_key =

@app.route("/")
def index():
    response = mysql.simple_community()
    public = mysql.public_notice()
    return render_template('index.html', response=response, public=public)

@app.route("/community_information")
def information():
    return render_template('information.html')


if __name__ == '__main__':
    app.run(debug=True,port=80)