from flask import Flask, render_template, request
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(2).csv")
app = Flask(__name__)

rows = len(df.axes[0])
n = 0

top1 = df.head(1)
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/sortPage")
def sortPage():
    return render_template("sortPage.html")

@app.route("/result", methods = ["POST", "GET"])
def result():
    output = request.form.to_dict()
    name = output["name"]
    if name.lower() == "writing tools":
        newDF = df[(df["Product Type"]) == "Writing Tools"]
        name = str(newDF.head())
    else:
        name = "not sort"

    return render_template("sortPage.html", name = name)
if __name__ == "__main__":
    app.run(debug=True)
