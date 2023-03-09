from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)
def get_random_item():
    df = pd.read_csv("database.csv")
    random_item = df.sample()
    return random_item.values.tolist()[0]

@app.route('/')
@app.route('/random')
def index():
    random_item = get_random_item()
    return render_template('random.html', random_item=random_item)

if __name__ == "__main__":
    app.run(debug=True)

