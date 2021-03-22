from flask import Flask, render_template, request, redirect
from dev_tests.JLPT_LVL_script import split_japanese
from dev_tests.JLPT_LVL_youtube import JLPT_lvl_core, get_yt_sub

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if "nm" in request.form:
            text = request.form["nm"]
            result = split_japanese(text)
            CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1 = JLPT_lvl_core(text, "Expression", 1)

            return render_template("helper.html", result=result, text=text, CORE_N5=CORE_N5, CORE_N4=CORE_N4,
                               CORE_N3=CORE_N3, CORE_N2=CORE_N2, CORE_N1=CORE_N1, mimetype='text/html')

        if "youtube" in request.form:
            video_id = request.form["youtube"]
            video_id = video_id.split("https://www.youtube.com/watch?v=",1)[1]
            text = get_yt_sub(video_id).to_string(header=False, index=False, index_names=False).replace('\n', '').replace(' ', '').replace('[', ' ').replace(']', ' ')
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