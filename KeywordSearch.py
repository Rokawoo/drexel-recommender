from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

test = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(2).csv")

# returns the user search bar KeyWeb.html page.
@app.route('/')
def index():
    return render_template('KeyWeb.html')

# Search function
# resultSearch.html is where search results will be outputted
@app.route('/search', methods=['POST'])
def search():
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
        return render_template('resultSearch.html', error=False, results=results)

# Allows user to click on website links and redirects to the official Drexel University Store
@app.route('/WebLinks/<string:link>', methods=['GET'])
def weblink(link):
    return redirect(link)

# Main program call
if __name__ == "__main__":
    app.run()
