from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
@app.route('/random')
def random():
    df = pd.read_csv("database.csv")
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

    return render_template('random.html', everything=everything, name=nameTitle, price=priceTitle,
                           link=linkTitle, imageTitle=imageTitle, categoryTitle=categoryTitle)


if __name__ == "__main__":
    app.run(debug=True)

