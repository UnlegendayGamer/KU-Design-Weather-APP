# import flast module
from flask import Flask, render_template, request
import readfile

# instance of flask application
app = Flask(__name__)

# home route that returns below text when root url is accessed
@app.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        print("A Button pressed!")
        submit_button = request.form.get("submit_button")
        other_button = request.form.get("other_button")
        if submit_button:
            readfile.getDict("weatherdata.txt")
            print("Submit button is pressed!")
        elif other_button:
            print("Other button is pressed!")
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)