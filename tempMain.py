from flask import Flask, render_template, request, session
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(2).csv")
app = Flask(__name__)
app.secret_key = "asfasdfasdfasdfasdf"
rows = len(df.axes[0])

top1 = df.head(1)

@app.route("/") #as soon as you log into
@app.route("/home") #home page
def home():
    a = 0
    session["a"] = a
    return render_template("home.html")

@app.route("/sortPage") #searchPage
def sortPage():
    return render_template("sortPage.html")

'''
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
'''
'''
@app.route("/writingToolsOutput", methods = ["POST", "GET"])
def writingToolsOutput():
    n = session.get("a")
    newDF = df[(df["Product Type"]) == "Writing Tools"]
    nameDF = newDF.loc[:,"Name"]
    priceDF = newDF.loc[:,"Price"]
    linkDF = newDF.loc[:,"WebLinks"]
    #name output
    name1 = str(nameDF.loc[n])
    name2 = str(nameDF.loc[n + 1])
    name3 = str(nameDF.loc[n + 2])
    name4 = str(nameDF.loc[n + 3])
    name5 = str(nameDF.loc[n + 4])
    name6 = str(nameDF.loc[n + 5])
    name7 = str(nameDF.loc[n + 6])
    name8 = str(nameDF.loc[n + 7])
    name9 = str(nameDF.loc[n + 8])
    name10 = str(nameDF.loc[n + 9])

    #price output
    price1 = str(priceDF.loc[n])
    price2 = str(priceDF.loc[n + 1])
    price3 = str(priceDF.loc[n + 2])
    price4 = str(priceDF.loc[n + 3])
    price5 = str(priceDF.loc[n + 4])
    price6 = str(priceDF.loc[n + 5])
    price7 = str(priceDF.loc[n + 6])
    price8 = str(priceDF.loc[n + 7])
    price9 = str(priceDF.loc[n + 8])
    price10 = str(priceDF.loc[n + 9])
    #session["a"] = session["a"] + 1
    return render_template("writingToolsPage.html", name1 = name1, name2 = name2, name3 = name3,
                           name4 = name4, name5 = name5, name6 = name6, name7 = name7, name8 = name8,
                           name9 = name9, name10 = name10, price1 = price1, price2 = price2,
                           price3 = price3, price4 = price4, price5 = price5, price6 = price6,
                           price7 = price7, price8 = price8, price9 = price9, price10 = price10)
'''
@app.route("/subtractCounter", methods = ["POST"])
def subtractCounter():
    n = session.get("a")
    newDF = df[(df["Product Type"]) == "Writing Tools"]
    nameDF = newDF.loc[:, "Name"]
    priceDF = newDF.loc[:, "Price"]
    linkDF = newDF.loc[:, "WebLinks"]
    total = len(newDF.index)
    n = n % total
    # name output
    name1 = str(nameDF.loc[n])
    name2 = str(nameDF.loc[n + 1])
    name3 = str(nameDF.loc[n + 2])
    name4 = str(nameDF.loc[n + 3])
    name5 = str(nameDF.loc[n + 4])
    name6 = str(nameDF.loc[n + 5])
    name7 = str(nameDF.loc[n + 6])
    name8 = str(nameDF.loc[n + 7])
    name9 = str(nameDF.loc[n + 8])
    name10 = str(nameDF.loc[n + 9])

    # price output
    price1 = str(priceDF.loc[n])
    price2 = str(priceDF.loc[n + 1])
    price3 = str(priceDF.loc[n + 2])
    price4 = str(priceDF.loc[n + 3])
    price5 = str(priceDF.loc[n + 4])
    price6 = str(priceDF.loc[n + 5])
    price7 = str(priceDF.loc[n + 6])
    price8 = str(priceDF.loc[n + 7])
    price9 = str(priceDF.loc[n + 8])
    price10 = str(priceDF.loc[n + 9])
    session["a"] = session["a"] - 1

    # link output
    link1 = str(linkDF.loc[n])
    link2 = str(linkDF.loc[n + 1])
    link3 = str(linkDF.loc[n + 2])
    link4 = str(linkDF.loc[n + 3])
    link5 = str(linkDF.loc[n + 4])
    link6 = str(linkDF.loc[n + 5])
    link7 = str(linkDF.loc[n + 6])
    link8 = str(linkDF.loc[n + 7])
    link9 = str(linkDF.loc[n + 8])
    link10 = str(linkDF.loc[n + 9])

    return render_template("writingToolsPage.html", name1=name1, name2=name2, name3=name3,
                           name4=name4, name5=name5, name6=name6, name7=name7, name8=name8,
                           name9=name9, name10=name10, price1=price1, price2=price2,
                           price3=price3, price4=price4, price5=price5, price6=price6,
                           price7=price7, price8=price8, price9=price9, price10=price10,
                           link1=link1, link2=link2, link3=link3, link4=link4,
                           link5=link5, link6=link6, link7=link7, link8=link8,
                           link9=link9, link10=link10)

@app.route("/addCounter", methods = ["POST"])
def addCounter():
    n = session.get("a")
    newDF = df[(df["Product Type"]) == "Writing Tools"]
    nameDF = newDF.loc[:, "Name"]
    priceDF = newDF.loc[:, "Price"]
    linkDF = newDF.loc[:, "WebLinks"]
    total = len(newDF.index)
    n = n % total
    # name output
    name1 = str(nameDF.loc[n])
    name2 = str(nameDF.loc[n + 1])
    name3 = str(nameDF.loc[n + 2])
    name4 = str(nameDF.loc[n + 3])
    name5 = str(nameDF.loc[n + 4])
    name6 = str(nameDF.loc[n + 5])
    name7 = str(nameDF.loc[n + 6])
    name8 = str(nameDF.loc[n + 7])
    name9 = str(nameDF.loc[n + 8])
    name10 = str(nameDF.loc[n + 9])

    # price output
    price1 = str(priceDF.loc[n])
    price2 = str(priceDF.loc[n + 1])
    price3 = str(priceDF.loc[n + 2])
    price4 = str(priceDF.loc[n + 3])
    price5 = str(priceDF.loc[n + 4])
    price6 = str(priceDF.loc[n + 5])
    price7 = str(priceDF.loc[n + 6])
    price8 = str(priceDF.loc[n + 7])
    price9 = str(priceDF.loc[n + 8])
    price10 = str(priceDF.loc[n + 9])
    session["a"] = session["a"] + 1

    #link output
    link1 = str(linkDF.loc[n])
    link2 = str(linkDF.loc[n + 1])
    link3 = str(linkDF.loc[n + 2])
    link4 = str(linkDF.loc[n + 3])
    link5 = str(linkDF.loc[n + 4])
    link6 = str(linkDF.loc[n + 5])
    link7 = str(linkDF.loc[n + 6])
    link8 = str(linkDF.loc[n + 7])
    link9 = str(linkDF.loc[n + 8])
    link10 = str(linkDF.loc[n + 9])

    return render_template("writingToolsPage.html", name1=name1, name2=name2, name3=name3,
                           name4=name4, name5=name5, name6=name6, name7=name7, name8=name8,
                           name9=name9, name10=name10, price1=price1, price2=price2,
                           price3=price3, price4=price4, price5=price5, price6=price6,
                           price7=price7, price8=price8, price9=price9, price10=price10,
                           link1 = link1, link2 = link2, link3 = link3, link4 = link4,
                           link5 = link5, link6 = link6, link7 = link7, link8 = link8,
                           link9 = link9, link10 = link10)



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

@app.route("/goBackWritingToolsPage", methods = ["POST"])
def goBackWritingToolsPage():
    return render_template("writingToolsPage.html")

if __name__ == "__main__":
    app.run(debug=True)
