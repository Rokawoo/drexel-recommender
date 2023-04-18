# Keyword Search program

from flask import Flask, render_template, request, redirect
from spellchecker import SpellChecker
import pandas as pd

app = Flask(__name__)

database = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(2).csv")

spell = SpellChecker(language = 'en')

# returns the user search bar html page.
@app.route('/')
def index():
    return render_template('KeyWeb.html')

# Noticed that the results dictionary was repeating in my code, made results dictionary a function. (4/13/2023)
def results_dictionary(row):
    result_dict = {}
    result_dict['Name'] = row['Name']
    result_dict['Price'] = row['Price']
    result_dict['Product Type'] = row['Product Type']
    result_dict['WebLinks'] = row['WebLinks']
    return result_dict

# Search function
# resultSearch.html is where search results will be outputted
@app.route('/search', methods=['POST'])
def search():
    keyword = request.form.get('keyword', '') # Get keyword from form
    suggestion = request.args.get('suggestion', '') # Get suggestion from query parameter
    if suggestion:
        keyword = suggestion
    matchKeyword = database[database['Name'].str.contains(keyword, case=False)]
    if len(matchKeyword) == 0:
        misspelled = spell.unknown([keyword])
        if misspelled:
            suggestions = spell.candidates(misspelled.pop())
            return render_template('KeyWeb.html', error=True, suggestions=suggestions)
        else:
            return render_template('KeyWeb.html', error=True)
    else:
        results = []
        for index, row in matchKeyword.iterrows():
            result = results_dictionary(row)
            results.append(result)
        return render_template('KeyWeb.html', error=False, results=results, keyword=keyword)


@app.route('/spell_check', methods=['GET', 'POST'])
def spell_check():
    keyword = request.args.get('keyword') or request.form.get('keyword', '') # Get keyword from query parameter or form
    misspelled = spell.unknown([keyword])
    if len(misspelled) > 0:
        suggestions = spell.candidates(keyword)
        return render_template('KeyWeb.html', error = True, suggestions = suggestions, keyword = keyword)
    else:
        # No misspelled words found, so just return the search results
        matchKeyword = database[database['Name'].str.contains(keyword, case = False)]
        if len(matchKeyword) == 0:
            # No results found, so return a "no results found" message
            return render_template('KeyWeb.html', error = True)
        else:
            # Results found, so return them to the user
            # Added the fix for the user to click on the suggestion words to return the product results in the database. 4/09/23
            # Formatting removing redundant code 4/13/23
            results = []
            for index, row in matchKeyword.iterrows():
                result =results_dictionary(row)
                results.append(result)
            return render_template('KeyWeb.html', error = False, results = results, keyword = keyword)

# Allows user to click on website links and redirects to the official Drexel University Store
@app.route('/WebLinks/<string:link>', methods=['GET'])
def weblink(link):
    return redirect(link)

# Main program call
if __name__ == "__main__":
    app.run()
