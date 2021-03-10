from JLPT_Youtube.scripts.JLPT_LVL_script import split_japanese
from flask import Flask, jsonify

from JLPT_Youtube_front.website import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug = True)



"""script = input("Past script:")

print("oui")
print(split_japanese(script))
print("oui")"""