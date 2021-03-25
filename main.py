from flask import Flask, render_template, request, redirect
from dev_tests.JLPT_LVL_script import get_traduction_10_jp_words, split_japanese
from dev_tests.JLPT_LVL_youtube import JLPT_lvl_core, get_yt_sub, get_JLPT_words

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        if "nm" in request.form:
            text_raw = request.form["nm"]
            result = get_traduction_10_jp_words(text_raw)
            CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1 = JLPT_lvl_core(text_raw, 1)

            column_list = ['vocab', 'count_x', 'Meaning', 'Reading']

            text= split_japanese(text_raw)
            df_5 = get_JLPT_words(text, 5)[column_list].to_html()
            df_4 = get_JLPT_words(text, 4)[column_list].to_html()
            df_3 = get_JLPT_words(text, 3)[column_list].to_html()
            df_2 = get_JLPT_words(text, 2)[column_list].to_html()
            df_1 = get_JLPT_words(text, 1)[column_list].to_html()

            return render_template("helper.html", result=result, text=text_raw, CORE_N5=CORE_N5, CORE_N4=CORE_N4,
                               CORE_N3=CORE_N3, CORE_N2=CORE_N2, CORE_N1=CORE_N1, mimetype='text/html', df_5=df_5,
                                   df_4=df_4, df_3=df_3, df_2=df_2, df_1=df_1)

        if "youtube" in request.form:
            video_id = request.form["youtube"]
            video_id = video_id.split("https://www.youtube.com/watch?v=",1)[1]
            text = get_yt_sub(video_id).to_string(header=False, index=False, index_names=False).replace('\n', '').replace(' ', '').replace('[', ' ').replace(']', ' ')
            result = get_traduction_10_jp_words(text)
            CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1 = JLPT_lvl_core(text, 1)

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