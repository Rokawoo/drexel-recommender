from flask import Flask, render_template, request, session
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(2).csv")
app = Flask(__name__)
app.secret_key = "asfasdfasdfasdfasdf"
rows = len(df.axes[0])

top1 = df.head(1)

@app.route("/") #as soon as you log into
@app.route("/home")
def home():
    a = 0
    session["a"] = a
    return render_template("home.html")

@app.route("/sortPage")
def sortPage():
    return render_template("sortPage.html")

@app.route("/result", methods = ["POST", "GET"])
def result():
    n = session.get("a")
    output = request.form.to_dict()
    name = output["name"]
    if name.lower() == "writing tools":
        #n = session.get["n", None]
        newDF = df[(df["Product Type"]) == "Writing Tools"]
        newDF = newDF.drop(["WebLinks"], axis=1)
        name = str(newDF.loc[n])
        name2 = str(newDF.loc[n + 1])
        name3 = str(newDF.loc[n + 2])
        session["a"] = session["a"] + 1
    else:
        name = "Invalid"
    print(n)
    print(session["a"])
    return render_template("sortPage.html", name = name, name2 = name2, name3 = name3)

@app.route("/goBackHome", methods = ["POST"])
def goBackHome():
    return render_template("home.html")

@app.route("/goBackSort", methods = ["POST"])
def goBackSort():
    return render_template("sortPage.html")

@app.route("/logout", methods = ["POST"])
def logout():
    session.pop("number", None)
    return render_template("sortPage.html")

if __name__ == "__main__":
    app.run(debug=True)
