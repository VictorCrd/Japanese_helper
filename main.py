from flask import Flask, render_template, request, redirect
from dev_tests.JLPT_LVL_script import split_japanese
from dev_tests.JLPT_LVL_youtube import JLPT_lvl_core

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        text = request.form["nm"]
        result = split_japanese(text)
        CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1 = JLPT_lvl_core(text, "Expression", 1)

        return render_template("helper.html", result=result, text=text, CORE_N5=CORE_N5, CORE_N4=CORE_N4,
                               CORE_N3=CORE_N3, CORE_N2=CORE_N2, CORE_N1=CORE_N1, mimetype='text/html')

    else:
        return render_template("index.html")


@app.route('/return', methods = ['POST', 'GET'])
def verify():
    if request.method == 'POST':

        return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)