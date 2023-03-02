from flask import Flask, render_template, redirect, session, url_for, request
import pandas as pd

df = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(2).csv")

ascendingDF = df.sort_values(by="Price", ascending=True)
descendingDF = df.sort_values(by="Price", ascending=False)

app = Flask(__name__)
app.secret_key = "asfasdfasdfasdfasdf"
rows = len(df.axes[0])

@app.route("/") #as soon as you log into
@app.route("/home") #home page
def home():
    counter = 0
    session["counter"] = counter
    ascending = False
    session["ascending"] = ascending
    category = "Writing Tools"
    session["Category"] = category
    return render_template("home.html")

@app.route("/sortPage") #searchPage
def sortPage():
    return render_template("sortPage.html")

@app.route("/goBackHome", methods = ["POST"])
def goBackHome():
    return render_template("home.html")

@app.route("/goBackWritingToolsPage", methods = ["POST"])
def goBackWritingToolsPage():
    defaultDFList = df
    if session["ascending"] == True:
        defaultDFList = ascendingDF
    elif session["ascending"] == False:
        defaultDFList = descendingDF

    nameDF = defaultDFList.loc[:, "Name"]
    priceDF = defaultDFList.loc[:, "Price"]
    linkDF = defaultDFList.loc[:, "WebLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList)
    return render_template("writingToolsPage.html", everything = everything)

@app.route("/addCounter", methods = ["POST"])
def addCounter():
    n = session["counter"]
    if session["Category"] == "Tech":
        techDF = df[(df["Product Type"]) == "Tech"] #do the price thing here
        nameDF = techDF.loc[:, "Name"]
        priceDF = techDF.loc[:, "Price"]
        linkDF = techDF.loc[:, "WebLinks"]

        return render_template("writingToolsPage.html")
    elif session["Category"] == "Writing Tools":
        return render_template("writingToolsPage.html")
    elif session["Category"] == "Art Supplies":
        return render_template("writingToolsPage.html")

@app.route("/ascendingButton", methods = ["POST"])
def ascendingButton():
    #df = df.sort_values(by="Price", ascending=True)
    session["ascending"] = True
    return ('', 204) #this is to return "nothing"

@app.route("/descendingButton", methods = ["POST"])
def descendingButton():
    session["ascending"] = False
    return ('', 204)

@app.route("/priceRange", methods = ["POST"])
def priceRange():
    upperBound = request.form["upperBound"]
    lowerBound = request.form["lowerBound"]
    print(upperBound)
    print(lowerBound)
    return ('', 204)

@app.route("/changeToTech", methods = ["POST"])
def changeToTech():
    session["Category"] = "Tech"
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    techDF = defaultDF[(defaultDF["Product Type"]) == "Tech"]
    nameDF = techDF.loc[:, "Name"]
    priceDF = techDF.loc[:, "Price"]
    linkDF = techDF.loc[:, "WebLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList)
    return render_template("writingToolsPage.html", everything = everything)

@app.route("/changeToArtSupplies", methods = ["POST"])
def changeToArtSupplies():
    session["Category"] = "Art Supplies"
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    artDF = defaultDF[(defaultDF["Product Type"]) == "Art Supplies"]
    nameDF = artDF.loc[:, "Name"]
    priceDF = artDF.loc[:, "Price"]
    linkDF = artDF.loc[:, "WebLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList)
    return render_template("writingToolsPage.html", everything = everything)

@app.route("/changeToWritingTools", methods = ["POST"])
def changeToWritingTools():
    session["Category"] = "Writing Tools"
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    writingToolsDF = defaultDF[(defaultDF["Product Type"]) == "Writing Tools"]
    nameDF = writingToolsDF.loc[:, "Name"]
    priceDF = writingToolsDF.loc[:, "Price"]
    linkDF = writingToolsDF.loc[:, "WebLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList)
    return render_template("writingToolsPage.html", everything = everything)

if __name__ == "__main__":
    app.run(debug=True)
