from flask import Flask, render_template, request, redirect
from dev_tests.JLPT_LVL_script import get_top_10_words, jlpt_lvl_core, get_jlpt_words, get_top_10_known_words, get_lemma
from dev_tests.youtube_subs import get_yt_sub
from dev_tests.speed_of_speach import get_speed_of_speach
from dev_tests.manage_known_words import add_known_word
from dev_tests.japanese_word_management import split_japanese

import numpy as np

application = Flask(__name__)

@application.route("/", methods=["POST", "GET"])
def helper():
    global top_10, text
    cnt_sum = 1  # 0= sum() & 1 = count()
    if request.method == "POST":
        speed_of_speech = 0
        video_id = 0

        if "nm" in request.form:
            text = request.form["nm"]

        if "youtube" in request.form:
            video_id = request.form["youtube"]
            video_id = video_id[video_id.find("https://www.youtube.com/watch?v=")+len("https://www.youtube.com/watch?v="):video_id.find("&")]
            #video_id = video_id.split("https://www.youtube.com/watch?v=", 1)[1]
            youtube_subs = get_yt_sub(video_id)
            speed_of_speech = get_speed_of_speach(youtube_subs)
            text = youtube_subs['phrases'].to_string(header=False, index=False).replace('\n', '').replace(' ', '')

        CORE_N5, CORE_N4, CORE_N3, CORE_N2, CORE_N1 = jlpt_lvl_core(text, cnt_sum)

        column_list = ['Vocab', 'Count', 'Meaning', 'Reading']

        text_jlpt = split_japanese(text)
        df_5 = get_jlpt_words(text_jlpt, 5)[column_list]
        df_4 = get_jlpt_words(text_jlpt, 4)[column_list]
        df_3 = get_jlpt_words(text_jlpt, 3)[column_list]
        df_2 = get_jlpt_words(text_jlpt, 2)[column_list]
        df_1 = get_jlpt_words(text_jlpt, 1)[column_list]

        lemma = get_lemma(text_jlpt)[0:10]

        top_10 = get_top_10_words(df_5, df_4, df_3, df_2, df_1)
        top_10['Known word'] = np.NaN
        for i in range(0, 10):
            top_10.loc[i:i + 1, 'Known word'] = '<a href="#" name="%d" id="add"><button class="btn-small waves-effect ' \
                                                'waves-light blue darken-1" type="submit" title="Add this word to ' \
                                                'known words, this word wont be shown next time you encounter ' \
                                                'it">Add</button></a>' % i

        df_top_10_known_words = get_top_10_known_words(df_5, df_4, df_3, df_2, df_1)
        print(df_top_10_known_words)
        if df_top_10_known_words.empty:
            print('DataFrame is empty!')
            df_top_10_known_words = int(0)
            print(df_top_10_known_words)
        else:
            df_top_10_known_words = df_top_10_known_words.to_html(escape=False)

        return render_template("helper.html",
                               top_10_words=top_10.to_html(escape=False),
                               top_10_lemma=lemma.to_html(escape=False),
                               text=text, CORE_N5=CORE_N5, CORE_N4=CORE_N4, CORE_N3=CORE_N3, CORE_N2=CORE_N2,
                               CORE_N1=CORE_N1, mimetype='text/html', df_5=df_5.to_html(),
                               df_4=df_4.to_html(), df_3=df_3.to_html(), df_2=df_2.to_html(), df_1=df_1.to_html(),
                               speed_of_speech=speed_of_speech,
                               video_id=video_id, known_words=df_top_10_known_words)

    else:
        return render_template("index.html")


@application.route('/return', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        return redirect("/")


@application.route('/background_process_test')
def background_process_test():
    print(top_10)
    # name = request.form['name']
    print("name")
    name = request.args.get('name')
    print(name)
    add_known_word(top_10, name)
    return "nothing"


if __name__ == '__main__':
    application.run()