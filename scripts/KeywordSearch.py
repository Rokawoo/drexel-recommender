# Keyword Search Program

from flask import Flask, render_template, request, redirect
from spellchecker import SpellChecker
import pandas as pd

app = Flask(__name__)

database = pd.read_csv("https://raw.githubusercontent.com/22lorenlei/test/main/Database%20-%20Sheet1%20(3).csv")

spell = SpellChecker(language='en')

# List of blocked words
blocked_words = {'arse', 'arsehead', 'arsehole', 'ass', 'asshole', 'bastard', 'bitch', 'bloody', 'bollocks', 'brotherfucker', 'bugger', 'bullshit', 'child-fucker', 'christ on a bike', 'christ on a cracker', 'cock', 'cocksucker', 'crap', 'cunt', 'damn', 'dick', 'dickhead', 'dyke', 'fatherfucker', 'frigger', 'fuck', 'goddamn', 'godsdamn', 'hell', 'holy shit', 'horseshit', 'in shit', 'jesus christ', 'jesus fuck', 'kike', 'motherfucker', 'nigga', 'nigger', 'nigra', 'piss', 'prick', 'pussy', 'shit', 'shit ass', 'shite', 'sisterfucker', 'slut', 'son of a bitch', 'son of a whore', 'spastic', 'sweet jesus', 'turd', 'twat', 'wanker'}

# Maximum number of suggestions to show for spell checker
max_suggestions = 10

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
    keyword = request.args.get('keyword') or request.form.get('keyword', '')  # Get keyword from query parameter or form
    keyword = filter_blocked_words(keyword)  # Filter out blocked words from keyword
    misspelled = spell.unknown([keyword])
    if len(misspelled) > 0:
        suggestions = spell.candidates(keyword)
        suggestions = [suggestion for suggestion in suggestions if suggestion not in blocked_words] # Filter out blocked words from suggestions
        suggestions = suggestions[:max_suggestions] # max number of suggestions for spell checker
        return render_template('KeyWeb.html', error=True, suggestions=suggestions, keyword=keyword)
    else:
        # No misspelled words found, so just return the search results
        matchKeyword = database[database['Name'].str.contains(keyword, case=False)]
        if len(matchKeyword) == 0:
            # No results found, so return a "no results found" message
            return render_template('KeyWeb.html', error=True)
        else:
            # Results found, so return them to the user
            results = []
            for index, row in matchKeyword.iterrows():
                result = results_dictionary(row)
                results.append(result)
            return render_template('KeyWeb.html', error = False, results = results, keyword = keyword)


# Allows user to click on website links and redirects to the official Drexel University Store
@app.route('/WebLinks/<string:link>', methods=['GET'])
def weblink(link):
    return redirect(link)

# Main program call
if __name__ == "__main__":
    app.run(debug=True)
