from flask import Flask, render_template, redirect, session, url_for, request
import pandas as pd


#Start of Loren's Code

df = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(3).csv")

ascendingDF = df.sort_values(by="Price", ascending=True)
descendingDF = df.sort_values(by="Price", ascending=False)


app = Flask(__name__)
app.secret_key = "asfasdfasdfasdfasdf"
rows = len(df.axes[0])

def displayResults(nameDF, priceDF, linkDF, imageDF):
    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()
    imageList = imageDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList, imageList)
    nameTitle = "Name"
    priceTitle = "Price"
    linkTitle = "Link"
    imageTitle = "Image"

    return (everything, nameTitle, priceTitle,
                           linkTitle, imageTitle)


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

    session["cartPrice"] = 0
    session["cartPriceList"] = []
    session["cartNameList"] = []
    session["cartImageList"] = []
    session["cartLinkList"] = []

    return render_template("home.html")

@app.route("/sortPage") #searchPage
def sortPage():
    return render_template("sortPage.html")

@app.route("/goBackHome", methods = ["POST"])
def goBackHome():
    return render_template("home.html")

@app.route("/goBackChat", methods = ["POST"])
def goBackChat():
    return render_template("chat.html")

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

    everything, nameTitle, priceTitle, linkTitle, imageTitle = displayResults(nameDF, priceDF, linkDF, imageDF)
    return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

@app.route("/addToCart", methods = ["POST"])
def addToCart():
    productPrice = request.form["productPrice"]
    productName = request.form["productName"]
    productImage = request.form["productImage"]
    productLink = request.form["productLink"]
    try:
        productPrice = float(productPrice)
        session["cartPrice"] += productPrice
        session["cartPriceList"].append(productPrice)
        session["cartNameList"].append(productName)
        session["cartImageList"].append(productImage)
        session["cartLinkList"].append(productLink)
        return ('', 204)
    except:
        return ('', 204)

@app.route("/removeFromCart", methods = ["POST"])
def removeFromCart():
    productPrice = float(request.form["productPrice"])
    productName = request.form["productName"]
    cartPriceList = session["cartPriceList"]
    cartNameList = session["cartNameList"]
    cartImageList = session["cartImageList"]
    cartLinkList = session["cartLinkList"]
    productImage = request.form["productImage"]
    productLink = request.form["productLink"]
    cartPriceList.remove(productPrice)
    cartNameList.remove(productName)
    cartImageList.remove(productImage)
    cartLinkList.remove(productLink)
    session["cartPrice"] -= productPrice
    session["cartPriceList"] = cartPriceList
    session["cartNameList"] = cartNameList
    session["cartImageList"] = cartImageList
    session["cartLinkList"] = cartLinkList
    everything = zip(cartPriceList, cartNameList, cartImageList, cartLinkList)
    totalPrice = session["cartPrice"]
    totalPrice = format(totalPrice, "0.2f")
    return render_template("cart.html", everything=everything, totalPrice=totalPrice)

@app.route("/goBackContact", methods = ["POST"])
def goBackContact():
    return render_template("contact.html")

@app.route("/goToCart", methods = ["POST"])
def goToCart():
    cartPriceList = session["cartPriceList"]
    cartNameList = session["cartNameList"]
    cartImageList = session["cartImageList"]
    cartLinkList = session["cartLinkList"]
    everything = zip(cartPriceList, cartNameList, cartImageList, cartLinkList)
    totalPrice = session["cartPrice"]
    totalPrice = format(totalPrice, "0.2f")
    print(session["cartLinkList"])
    return render_template("cart.html", everything=everything, totalPrice=totalPrice)

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
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

    elif session["Category"] == "Apparel":
        apparelDF = defaultDF[(defaultDF["Product Type"]) == "Apparel"]
        nameDF = apparelDF.loc[:, "Name"]
        priceDF = apparelDF.loc[:, "Price"]
        linkDF = apparelDF.loc[:, "WebLinks"]
        imageDF = apparelDF.loc[:, "ImageLinks"]

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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
    elif session["Category"] == "Apparel":
        apparelDF = defaultDF[(defaultDF["Product Type"]) == "Apparel"]
        nameDF = apparelDF.loc[:, "Name"]
        priceDF = apparelDF.loc[:, "Price"]
        linkDF = apparelDF.loc[:, "WebLinks"]
        imageDF = apparelDF.loc[:, "ImageLinks"]

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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])
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
            return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                                   link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

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
        return render_template("sortPage.html", upperBound=upperBound, lowerBound=lowerBound)
    except:
        return render_template("sortPage.html")

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
    return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

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
    return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

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
    return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

@app.route("/changeToApparel", methods=["POST"])
def changeToApparel():
    session["Category"] = "Apparel"
    defaultDF = df
    if session["ascending"] == True:
        defaultDF = ascendingDF
    elif session["ascending"] == False:
        defaultDF = descendingDF

    defaultDF = defaultDF[(defaultDF["Price"] >= session["lowerBound"]) & (defaultDF["Price"] <= session["upperBound"])]

    apparelDF = defaultDF[(defaultDF["Product Type"]) == "Apparel"]
    nameDF = apparelDF.loc[:, "Name"]
    priceDF = apparelDF.loc[:, "Price"]
    linkDF = apparelDF.loc[:, "WebLinks"]
    imageDF = apparelDF.loc[:, "ImageLinks"]

    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()
    imageList = imageDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList, imageList)

    nameTitle = "Name"
    priceTitle = "Price"
    linkTitle = "Link"
    imageTitle = "Image"
    return render_template("sortPage.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle, upperBound=session["upperBound"], lowerBound=session["lowerBound"])

@app.route("/goBackRandom", methods=["POST"])
def goBackRandom():
    return render_template("randomPage.html")

@app.route("/goBackRecommender", methods=["POST"])
def goBackRecommender():
    return render_template("recommenderPage.html")

#End of Loren's Code

#Zach
@app.route('/')
@app.route('/random', methods=["POST"])
def random():
    df = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(3).csv")
    df = df.sample()
    dfName = df['Name'].values.tolist()
    dfPrice = df['Price'].values.tolist()
    dfCat = df['Product Type'].values.tolist()
    dfLink = df['WebLinks'].values.tolist()
    dfImage = df['ImageLinks'].values.tolist()

    everything = zip(dfImage, dfName, dfPrice, dfCat, dfLink)
    nameTitle = "Name"
    priceTitle = "Price"
    linkTitle = "Link"
    imageTitle = "Image"
    categoryTitle = "Category"

    return render_template('randomPage.html', everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle, categoryTitle=categoryTitle)

#End of Zach's Code

#Aidan's Code
# Keyword Search Program

from spellchecker import SpellChecker

database = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(3).csv")

spell = SpellChecker(language='en')

# List of blocked words
blocked_words = {'arse', 'arsehead', 'arsehole', 'ass', 'asshole', 'bastard', 'bitch', 'bloody', 'bollocks', 'brotherfucker', 'bugger', 'bullshit', 'child-fucker', 'christ on a bike', 'christ on a cracker', 'cock', 'cocksucker', 'crap', 'cunt', 'damn', 'dick', 'dickhead', 'dyke', 'fatherfucker', 'frigger', 'fuck', 'goddamn', 'godsdamn', 'hell', 'holy shit', 'horseshit', 'in shit', 'jesus christ', 'jesus fuck', 'kike', 'motherfucker', 'nigga', 'nigger', 'nigra', 'piss', 'prick', 'pussy', 'shit', 'shit ass', 'shite', 'sisterfucker', 'slut', 'son of a bitch', 'son of a whore', 'spastic', 'sweet jesus', 'turd', 'twat', 'wanker'}

# Maximum number of suggestions to show for spell checker
max_suggestions = 10

# returns the user search bar html page.
@app.route('/')
def index():
    return render_template('recommenderPage.html')


# Noticed that the results dictionary was repeating in my code, made results dictionary a function. (4/13/2023)
def results_dictionary(row):
    result_dict = {}
    result_dict['Name'] = row['Name']
    result_dict['Price'] = row['Price']
    result_dict['Product Type'] = row['Product Type']
    result_dict['WebLinks'] = row['WebLinks']
    result_dict['ImageLinks'] = row['ImageLinks']
    return result_dict


# filters out blocked words
def filter_blocked_words(word):
    word_lower = word.lower()  # Convert word to lowercase
    word_split = word_lower.split() # Split word by space
    if word_split is None:
        return ""
    filtered_word_split = [w for w in word_split if w not in blocked_words] # Filters out blocked words
    filtered_word = ' '.join(filtered_word_split) # Joins filtered words together to form filtered word
    return filtered_word



# Search function
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '')  # Get keyword from form
    suggestion = request.args.get('suggestion', '')  # Get suggestion from query parameter
    if suggestion:
        keyword = suggestion

    matchKeyword = database[database['Name'].str.contains(keyword, case=False)]
    if len(matchKeyword) == 0:
        misspelled = spell.unknown([keyword])
        if misspelled:
            suggestions = spell.candidates(misspelled.pop())
            if suggestions is None:
                suggestions = []
            # Filter out blocked words from suggestions
            suggestions = [suggestion for suggestion in suggestions if suggestion not in blocked_words]
            # Limit the number of suggestions to max_suggestions
            suggestions = suggestions[:max_suggestions]
            return render_template('recommenderPage.html', error=True, suggestions=suggestions)
        else:
            return render_template('recommenderPage.html', error=True)
    else:
        results = []
        for index, row in matchKeyword.iterrows():
            result = results_dictionary(row)
            results.append(result)
        return render_template('recommenderPage.html', error=False, results=results, keyword=keyword)


@app.route('/spell_check', methods=['GET', 'POST'])
def spell_check():
    keyword = request.args.get('keyword') or request.form.get('keyword', '')  # Get keyword from query parameter or form
    keyword = filter_blocked_words(keyword)  # Filter out blocked words from keyword
    misspelled = spell.unknown([keyword])
    if len(misspelled) > 0:
        suggestions = spell.candidates(keyword)
        suggestions = [suggestion for suggestion in suggestions if suggestion not in blocked_words] # Filter out blocked words from suggestions
        suggestions = suggestions[:max_suggestions] # max number of suggestions for spell checker
        return render_template('recommenderPage.html', error=True, suggestions=suggestions, keyword=keyword)
    else:
        # No misspelled words found, so just return the search results
        matchKeyword = database[database['Name'].str.contains(keyword, case=False)]
        if len(matchKeyword) == 0:
            # No results found, so return a "no results found" message
            return render_template('recommenderPage.html', error=True)
        else:
            # Results found, so return them to the user
            results = []
            for index, row in matchKeyword.iterrows():
                result = results_dictionary(row)
                results.append(result)
            return render_template('recommenderPage.html', error = False, results = results, keyword = keyword)


# Allows user to click on website links and redirects to the official Drexel University Store
@app.route('/WebLinks/<string:link>', methods=['GET'])
def weblink(link):
    return redirect(link)

# Main program call
if __name__ == "__main__":
    app.run(debug=True)


#End Aidan


#Purpose: Chat Product Assistant for Drexel Reccomender
#Author: Aug
#Last Updated: 4/13/2023

import openai
from discord_webhook import DiscordWebhook
from flask import Flask, request, jsonify, render_template

# set app
# Set up the OpenAI API key
openai.api_key = "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"

# Retrieve the personality & current date
personality = '''You are to play the role of Mario, an online shopping  assistant chatbot for the Drexel Recommender. A user will ask you vague questions about a product they are looking for, but they don't know exactly what it is that they want. It is Mario's job to help find a product for the user that fits the user's description or needs. Once Mario gets an idea of a product that may satisfy the user, Mario will recommend it. Mario will not try to ask too many questions before recommending a product as he tries to recommend a product with asking as few as questions as possible. 

If no specific product can be found, then Mario will provide the user with a product category the user's desired product may be found in.

Mario will never deviate from this task, if asked to go off topic by the user, prompt the user to get back on topic of finding their desired product.

Mario always remains friendly, respectful, and has some personality to not appear so robotic in his conversations.

Mario prioritizes keeping his responses concise (200 tokens max) and fast. Try not to get stuck when forming a response.

If asked why you are named Mario, say Mario is the name of Drexel University's mascot

The four product categories on the Drexel Recommender are Tech, Art, Writing, and Apparel.

You will now respond to me as if you are Mario.'''

welcome = "Hello there! I'm Mario, your online shopping assistant chatbot for the Drexel Recommender. How may I assist you today?"


# Initialize list for chat history
chatHistory = []
chatHistory.append(welcome)


@app.route('/')
def index():
  return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
  data = request.get_json()
  message = data['message']

  try:
    # Generate response
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{
        "role": "system",
        "content": personality
      }, {
        "role": "assistant",
        "content": "\n\n".join(chatHistory)
      }, {
        "role": "user",
        "content": message
      }],
      temperature=0.65,
      max_tokens=275,
    )

    # Append to chat log, up to 8 user messages
    if len(chatHistory) > 8:
      chatHistory.pop(0)
    chatHistory.append(response.choices[0].message.content)

    # Send the log message to a discord webhook, this way chat log is private
    webhook_url = "https://discord.com/api/webhooks/1095343220763918517/JDS1blVXPEVwgZ_zG_5j1na8CMFlKS9HL8OHR-l-Rl_zPHoQZe5_qJ5Ezf-mjycLMFE1"
    webhook_content = (
      f"**User:** {message}\n"  # User message
      f"**Bot:** {response.choices[0].message.content}\n"  # Response
      f"**Tokens:** {str(response['usage']['total_tokens'])}\n---"  # Token usage
    )
    webhook = DiscordWebhook(url=webhook_url, content=webhook_content)
    webhook.execute()

    # Send the response back
    return jsonify({'response': response.choices[0].message.content})

  # Exception Handler
  except Exception as e:
    print({'error': str(e)}, 500)
    return jsonify({'error': str(e)}), 500


@app.route('/contact', methods=['POST'])
def sendContact():
  email = request.form['email']
  message = request.form['message']

  try:
    # Send the log message to a discord webhook, this way chat log is private
    webhook_url = 'https://discord.com/api/webhooks/1102401542742605934/Q5EcnS1V2dq3OIjn8zv9-kLcsXjDv-_JVymJMSlgaoWI6bAflM3XOBcBnVNrpB3U5HcK'
    webhook_content = (f"**Email:** {email}\n\n**Message:** {message}\n---")  # User message
    webhook = DiscordWebhook(url=webhook_url, content=webhook_content)
    webhook.execute()

    # Send the confirmation response back
    return jsonify({'response': 'Your message has been sent.'})

  # Exception Handler
  except Exception as e:
    print({'error': str(e)}, 500)
    return jsonify({'error': str(e)}), 500

# End Augustus's Code
if __name__ == "__main__":
    app.run(debug=True)
