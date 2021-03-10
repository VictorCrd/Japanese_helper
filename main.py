from flask import Flask, render_template, request
from dev_tests.JLPT_LVL_script import split_japanese

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        text = request.form["nm"]
        #return text, split_japanese(text)

        return split_japanese(text)
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)