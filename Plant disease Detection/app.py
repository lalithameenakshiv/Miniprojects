from flask import Flask, render_template, request
import subprocess
import os
import sys


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")



@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["image"]

    upload_path = "static/uploads/" + file.filename

    file.save(upload_path)


    result = subprocess.check_output(
        [
            sys.executable,
            "predict.py",
            upload_path
        ]
    )


    output = result.decode("utf-8")


    return render_template(
        "result.html",
        prediction=output,
        image=upload_path
    )



if __name__ == "__main__":
    app.run(debug=True)
    