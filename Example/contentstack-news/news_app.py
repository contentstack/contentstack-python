from flask import Flask, render_template, url_for
from contentstack import Stack

app = Flask(__name__)


def fetch_news():
    stack = Stack(api_key='blt920bb7e90248f607', access_token='blt0c4300391e033d4a59eb2857', environment='production')
    query = stack.content_type('news').query()
    response = query.find()
    return response


@app.route('/')
@app.route('/home')
def home():
    headlines = fetch_news()
    return render_template('home.html', news=headlines, title="home")


@app.route('/about')
def about():
    return render_template('about.html', title="about")


if __name__ == "__main__":
    app.run(debug=True)
