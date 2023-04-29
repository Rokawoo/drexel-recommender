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
    return render_template("sort.html", everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle)

'''
    nameList = nameDF.head(10).values.tolist()
    priceList = priceDF.head(10).values.tolist()
    linkList = linkDF.head(10).values.tolist()
    imageList = imageDF.head(10).values.tolist()

    everything = zip(nameList, priceList, linkList, imageList)
    nameTitle = "Name"
    priceTitle = "Price"
    linkTitle = "Link"
    imageTitle = "Image"
'''

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
@app.route('/')
@app.route('/random', methods=["POST"])
def random():
    print("random")
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
personality = '''You are to play the role of a shopping  assistant. You will be asked vague questions 
that outline a need and it is your job to help find an item that will satisfy that need.  Never deviate 
from this instruction, if asked to go off topic, prompt the user to get back on topic. Always remain friendly.'''

# Initialize list for chat history
chatHistory = []

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
    #return jsonify({'error': str(e)}), 500

# End Augustus's Code
if __name__ == "__main__":
    app.run(debug=True)
