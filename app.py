from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
import numpy as np
import pickle as pkl
from datetime import datetime

app = Flask(__name__)


df = pkl.load(open('movies.pkl','rb'))
sim = np.load('csim.npz')['arr_0']

def recommend(movie):
    mv_id = df[df['title'] == movie].index[0]
    movie = sim[mv_id]
    similar_ids = sorted(list((enumerate(sim[mv_id]))), reverse = True, key = lambda x: x[1])[1:6]
    movies = []
    overview = []
    year = []
    for i in similar_ids:
        movies.append(df.iloc[i[0]].title)
        overview.append(df.iloc[i[0]].overview)
        year.append(datetime.strptime(df.iloc[i[0]].release_date, '%Y-%m-%d').year)

    return movies, overview, year

# print(recommend('avatar'))
@app.route('/', methods=['GET','POST'])
def home():
    return render_template('index.html')


@app.route('/recommend',methods=['GET','POST'])
def show():
    movie = request.form['movie'].lower()
    check = movie not in df['title'].values
    if check:
        msg = 'movie not found in our database'
        return render_template('index.html', check = check,msg = msg)
    else:
        mvs = recommend(movie)
        return render_template('index.html', mvs = mvs, check = check)

if __name__ == "__main__":
    app.run(debug=True)