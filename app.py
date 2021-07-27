from flask import Flask, render_template, request, redirect
from dev_tests.manage_known_words import add_known_word


import numpy as np

app = Flask(__name__)

@app.route("/", methods=["POST", "GET"])
def helper():
    global top_10, text
    cnt_sum = 1  # 0= sum() & 1 = count()
    if request.method == "POST":
        speed_of_speech = 0


    else:
        return render_template("index.html")


@app.route('/return', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        return redirect("/")


@app.route('/background_process_test')
def background_process_test():
    print(top_10)
    # name = request.form['name']
    print("name")
    name = request.args.get('name')
    print(name)
    add_known_word(top_10, name)
    return "nothing"


if __name__ == '__main__':
    app.run()