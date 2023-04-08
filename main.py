from flask import Flask, render_template, redirect, session, url_for, request
import pandas as pd
import os

#Start of Loren's Code
imgFolder = os.path.join('static', 'img')

df = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(3).csv")

ascendingDF = df.sort_values(by="Price", ascending=True)
descendingDF = df.sort_values(by="Price", ascending=False)


app = Flask(__name__)
app.secret_key = "asfasdfasdfasdfasdf"
rows = len(df.axes[0])

app.config['UPLOAD_FOLDER'] = imgFolder

@app.route("/") #as soon as you log into
@app.route("/home") #home page
def home():
    counter = 0
    session["counter"] = counter
    ascending = False
    session["ascending"] = ascending
    category = "Writing Tools"
    session["Category"] = category

    session["upperBound"] = 5000.0
    session["lowerBound"] = 0.0

    return render_template("home.html")

@app.route("/sortPage") #searchPage
def sortPage():
    return render_template("sortPage.html")

@app.route("/goBackHome", methods = ["POST"])
def goBackHome():
    return render_template("home.html")

@app.route("/goBackSort", methods = ["POST"])
def goBackSort():
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    defaultDF = defaultDF[(defaultDF["Price"] >= session["lowerBound"]) & (defaultDF["Price"] <= session["upperBound"])]

    nameDF = defaultDF.loc[:, "Name"]
    priceDF = defaultDF.loc[:, "Price"]
    linkDF = defaultDF.loc[:, "WebLinks"]
    imageDF = defaultDF.loc[:, "ImageLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()
    imageList = imageDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList, imageList)
    nameTitle = "Name"
    priceTitle = "Price"
    linkTitle = "Link"
    imageTitle = "Image"

    drexelTopper = os.path.join(app.config['UPLOAD_FOLDER'], 'DrexelTopper.png')
    return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, drexelTopper = drexelTopper, imageTitle=imageTitle)

@app.route("/addCounter", methods = ["POST"])
def addCounter():
    session["counter"] += 1
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    defaultDF = defaultDF[(defaultDF["Price"] >= session["lowerBound"]) & (defaultDF["Price"] <= session["upperBound"])]

    if session["Category"] == "Tech":
        techDF = defaultDF[(defaultDF["Product Type"]) == "Tech"] #do the price thing here
        nameDF = techDF.loc[:, "Name"]
        priceDF = techDF.loc[:, "Price"]
        linkDF = techDF.loc[:, "WebLinks"]
        imageDF = techDF.loc[:, "ImageLinks"]

        nameList = nameDF.values.tolist()
        priceList = priceDF.values.tolist()
        linkList = linkDF.values.tolist()
        imageList = imageDF.values.tolist()

        limit = len(nameList)
        upper = 10 + session["counter"]
        lower = 0 + session["counter"]
        if limit == upper:
            upper = limit

        if len(nameList) <= 10:
            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("writingToolsPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)
        elif len(nameList) > 10:

            nameList = nameList[lower:upper]
            priceList = priceList[lower:upper]
            linkList = linkList[lower:upper]
            imageList = imageList[lower:upper]

            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)

    elif session["Category"] == "Writing Tools":
        writingDF = defaultDF[(defaultDF["Product Type"]) == "Writing Tools"]
        nameDF = writingDF.loc[:, "Name"]
        priceDF = writingDF.loc[:, "Price"]
        linkDF = writingDF.loc[:, "WebLinks"]
        imageDF = writingDF.loc[:, "ImageLinks"]

        nameList = nameDF.values.tolist()
        priceList = priceDF.values.tolist()
        linkList = linkDF.values.tolist()
        imageList = imageDF.values.tolist()

        limit = len(nameList)
        upper = 10 + session["counter"]
        lower = 0 + session["counter"]
        if limit == upper:
            upper = limit

        if len(nameList) <= 10:
            everything = zip(nameList, priceList, linkList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)
        elif len(nameList) > 10:

            nameList = nameList[lower:upper]
            priceList = priceList[lower:upper]
            linkList = linkList[lower:upper]
            imageList = imageList[lower:upper]

            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)

    elif session["Category"] == "Art Supplies":
        artSuppliesDF = defaultDF[(defaultDF["Product Type"]) == "Art Supplies"]
        nameDF = artSuppliesDF.loc[:, "Name"]
        priceDF = artSuppliesDF.loc[:, "Price"]
        linkDF = artSuppliesDF.loc[:, "WebLinks"]
        imageDF = artSuppliesDF.loc[:, "ImageLinks"]

        nameList = nameDF.values.tolist()
        priceList = priceDF.values.tolist()
        linkList = linkDF.values.tolist()
        imageList = imageDF.values.tolist()

        limit = len(nameList)
        upper = 10 + session["counter"]
        lower = 0 + session["counter"]
        if limit == upper:
            upper = limit

        if len(nameList) <= 10:
            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)
        elif len(nameList) > 10:

            nameList = nameList[lower:upper]
            priceList = priceList[lower:upper]
            linkList = linkList[lower:upper]
            imageList = imageList[lower:upper]

            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)

@app.route("/subtractCounter", methods = ["POST"])
def subtractCounter():
    session["counter"] -= 1
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    defaultDF = defaultDF[(defaultDF["Price"] >= session["lowerBound"]) & (defaultDF["Price"] <= session["upperBound"])]

    if session["Category"] == "Tech":
        techDF = defaultDF[(defaultDF["Product Type"]) == "Tech"]  # do the price thing here
        nameDF = techDF.loc[:, "Name"]
        priceDF = techDF.loc[:, "Price"]
        linkDF = techDF.loc[:, "WebLinks"]
        imageDF = techDF.loc[:, "ImageLinks"]

        nameList = nameDF.values.tolist()
        priceList = priceDF.values.tolist()
        linkList = linkDF.values.tolist()
        imageList = imageDF.values.tolist()

        limit = len(nameList)
        upper = 10 + session["counter"]
        lower = 0 + session["counter"]
        if limit == upper:
            upper = limit

        if len(nameList) <= 10:
            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)
        elif len(nameList) > 10:

            nameList = nameList[lower:upper]
            priceList = priceList[lower:upper]
            linkList = linkList[lower:upper]
            imageList = imageList[lower:upper]

            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)

    elif session["Category"] == "Writing Tools":
        writingDF = defaultDF[(defaultDF["Product Type"]) == "Writing Tools"]
        nameDF = writingDF.loc[:, "Name"]
        priceDF = writingDF.loc[:, "Price"]
        linkDF = writingDF.loc[:, "WebLinks"]
        imageDF = writingDF.loc[:, "ImageLinks"]

        nameList = nameDF.values.tolist()
        priceList = priceDF.values.tolist()
        linkList = linkDF.values.tolist()
        imageList = imageDF.values.tolist()

        limit = len(nameList)
        upper = 10 + session["counter"]
        lower = 0 + session["counter"]
        if limit == upper:
            upper = limit

        if len(nameList) <= 10:
            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)
        elif len(nameList) > 10:

            nameList = nameList[lower:upper]
            priceList = priceList[lower:upper]
            linkList = linkList[lower:upper]
            imageList = imageList[lower:upper]

            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)

    elif session["Category"] == "Art Supplies":
        artSuppliesDF = defaultDF[(defaultDF["Product Type"]) == "Art Supplies"]
        nameDF = artSuppliesDF.loc[:, "Name"]
        priceDF = artSuppliesDF.loc[:, "Price"]
        linkDF = artSuppliesDF.loc[:, "WebLinks"]
        imageDF = artSuppliesDF.loc[:, "ImageLinks"]

        nameList = nameDF.values.tolist()
        priceList = priceDF.values.tolist()
        linkList = linkDF.values.tolist()
        imageList = imageDF.values.tolist()

        limit = len(nameList)
        upper = 10 + session["counter"]
        lower = 0 + session["counter"]
        if limit == upper:
            upper = limit

        if len(nameList) <= 10:
            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)
        elif len(nameList) > 10:

            nameList = nameList[lower:upper]
            priceList = priceList[lower:upper]
            linkList = linkList[lower:upper]
            imageList = imageList[lower:upper]

            everything = zip(nameList, priceList, linkList, imageList)
            nameTitle = "Name"
            priceTitle = "Price"
            linkTitle = "Link"
            imageTitle = "Image"
            return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle)

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
    try:
        session["upperBound"] = float(upperBound)
        session["lowerBound"] = float(lowerBound)
        return ('', 204)
    except:
        return render_template("sort.html")

@app.route("/changeToTech", methods = ["POST"])
def changeToTech():
    session["Category"] = "Tech"
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    defaultDF = defaultDF[(defaultDF["Price"] >= session["lowerBound"]) & (defaultDF["Price"] <= session["upperBound"])]

    techDF = defaultDF[(defaultDF["Product Type"]) == "Tech"]
    nameDF = techDF.loc[:, "Name"]
    priceDF = techDF.loc[:, "Price"]
    linkDF = techDF.loc[:, "WebLinks"]
    imageDF = techDF.loc[:, "ImageLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()
    imageList = imageDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList, imageList)

    nameTitle = "Name"
    priceTitle = "Price"
    linkTitle = "Link"
    imageTitle = "Image"
    return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle)

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
    imageDF = artDF.loc[:, "ImageLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()
    imageList = imageDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList, imageList)

    nameTitle = "Name"
    priceTitle = "Price"
    linkTitle = "Link"
    imageTitle = "Image"
    return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle)

@app.route("/changeToSort", methods = ["POST"])
def changeToSort():
    session["Category"] = "Writing Tools"
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    defaultDF = defaultDF[(defaultDF["Price"] >= session["lowerBound"]) & (defaultDF["Price"] <= session["upperBound"])]

    writingToolsDF = defaultDF[(defaultDF["Product Type"]) == "Writing Tools"]
    nameDF = writingToolsDF.loc[:, "Name"]
    priceDF = writingToolsDF.loc[:, "Price"]
    linkDF = writingToolsDF.loc[:, "WebLinks"]
    imageDF = writingToolsDF.loc[:, "ImageLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()
    imageList = imageDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList, imageList)

    nameTitle = "Name"
    priceTitle = "Price"
    linkTitle = "Link"
    imageTitle = "Image"
    return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle)

@app.route("/goBackRandom", methods=["POST"])
def goBackRandom():
    return render_template("randomPage.html")

@app.route("/goBackRecommender", methods=["POST"])
def goBackRecommender():
    return render_template("recommenderPage.html")

#End of Loren's Code

#Zach
def get_random_item():
    df = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(2).csv")
    random_item = df.sample()
    return random_item.values.tolist()[0]
@app.route('/')
@app.route('/random', methods=["POST"])
def index():
    random_item = get_random_item()
    return render_template("randomPage.html", random_item=random_item)
#End of Zach's Code

#Aidan's Code
@app.route('/search', methods=['POST'])
def search():
    test = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(2).csv")
    keyword = request.form['keyword'] # Get keyword from form
    matchKeyword = test[test['Name'].str.contains(keyword, case=False)]
    if len(matchKeyword) == 0:
        return render_template('resultSearch.html', error=True)
    else:
        results = []
        for index, row in matchKeyword.iterrows():
            result_dict = {}
            result_dict['Name'] = row['Name']
            result_dict['Price'] = row['Price']
            result_dict['Product Type'] = row['Product Type']
            result_dict['WebLinks'] = row['WebLinks']
            results.append(result_dict)
        return render_template("recommenderPage.html", error=False, results=results)


# Allows user to click on website links and redirects to the official Drexel University Store
@app.route('/WebLinks/<string:link>', methods=['GET'])
def weblink(link):
    return redirect(link)

#End Aidan


if __name__ == "__main__":
    app.run(debug=True)
