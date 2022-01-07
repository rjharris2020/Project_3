from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


#web page routes 
@app.route("/")
def home(): 
    return render_template("home.html")

@app.route("/analysis")
def analysis(): 
    return render_template("analysis.html")

@app.route("/about")
def about():
    return  render_template("about.html")
    

if __name__ == "__main__": 
    app.run()