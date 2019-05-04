from flask import Flask, render_template, flash, request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from imdb import IMDb
import json
from collections import namedtuple
from threading import Thread
import time
from multiprocessing import Process,Value
import http.client
import json
import requests

application = Flask(__name__)
application.config['SECRET_KEY'] = '57ieiqw91628bb0b13ce0c676dfde280ba245'
option = None
chosenMovie = None
chosenRestaurant = None
Movie = namedtuple('Movie', 'Title Popularity Plot')
zipcode = None

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('Search')


@application.route("/", methods = ['POST','GET'])
def main():
    form = MyForm()
    if request.method == 'POST':
        global zipcode
        zipcode =  form.name.data
        return redirect(url_for('movie_lookup', movieID = form.name.data))
    else:
        return render_template('index.html',form = form)

@application.route('/movie/<movieID>', methods = ['POST','GET'])
def movie_lookup(movieID):
    form = MyForm()
    conn = http.client.HTTPSConnection("api.themoviedb.org")
    movieResults = []
    
    ia = IMDb()
    
    movies = ia.search_movie('spiderman')
    for item in movies:
        ia.update(item)

    conn = http.client.HTTPSConnection("api.themoviedb.org")

    print(item.get('title'), item.get('rating'), item.get('plot'))
    
    payload = "{}"

    conn.request("GET", "/3/movie/now_playing?page=1&language=en-US&api_key=4f8eb69d2b4817d88b7ca064921660c2", payload)

    res = conn.getresponse()
    data = res.read()

    data = data.decode("utf-8")

    data = json.loads(data)
    for movies in data['results']:
        m = Movie(movies['title'], movies['popularity'],movies['overview'])
        movieResults.append(m)

    end = time.time()

    if request.method == 'POST':
        option = request.form['options']
        for movie in movieResults:
            if option in movie.Title:
                global chosenMovie
                chosenMovie = movie.Title
        print(chosenMovie)
        return redirect( url_for('yelp_search'))
    else:
        return render_template("step1.html",form = form, movieResults = movieResults)

@application.route('/yelpSearch', methods = ['POST','GET'])
def yelp_search():
    form = MyForm()

    store = request.form.get('store')

    # Places API Key 

    # url variable store url 
    url = "https://maps.googleapis.com/maps/api/place/textsearch/json?query={}&key=AIzaSyBFNSAxslWL0c9xPc223PJGJFCu2hIZlGU".format(store)

    # The text string on which to search 
    res = requests.get(url)

    data = res.json()

    store = data['results']

    if request.method == 'POST':
       return render_template("handle_place.html", store = store)
    else:
        return render_template("step2.html")

@application.route('/weatherLookUp', methods = ['POST','GET'])
def get_forecast():
    form = MyForm()
 

    global zipcode
    days_forecast = get_weather(zipcode)
    print("ZIPCODE IS ", zipcode)
    print("SIZE OF DAYS", len(days_forecast))
    return render_template('handle_weather.html', days_forecast = days_forecast)

@application.route('/result', methods = ['POST','GET'])
def end_reccomendation():
    form = MyForm()
    if request.method == 'POST':
       return redirect( url_for('main'))
    else:
        return render_template("end_page.html",chosenMovie = chosenMovie)

def getMovieDetails(item,ia):
    print(item.get('title'))
    ia.update(item)
    m = Movie(item.get('title'), item.get('cast'), item.get('rating'), item.get('plot'))
    return "sa"

def get_weather(zipcode):  
    API_KEY = "45lPufUPF4XJ7tPjHiSNi0nIwoKG5Sh2"    # 50 requests per day
    LOC_URL = "http://dataservice.accuweather.com/locations/v1/search"
    FORECAST_URL = "http://dataservice.accuweather.com/forecasts/v1/daily/5day/"

    """ Get the location key from the zipcode """
    location_params = {'q':zipcode, 'apikey':API_KEY}
    location_answer = requests.get(url = LOC_URL, params = location_params)
    location_data = location_answer.json()
    location_key = location_data[0]['Key']
    
    """ Use location key to get 5 day forecast """
    forecast_params = {'apikey':API_KEY}
    forecast_answer = requests.get(url = (FORECAST_URL + location_key), params = forecast_params)
    forecast_data = forecast_answer.json()
    five_day = []

    for day in range(5):
        temp_max = forecast_data['DailyForecasts'][day]['Temperature']['Maximum']['Value']
        temp_min = forecast_data['DailyForecasts'][day]['Temperature']['Minimum']['Value']
        day_forecast = forecast_data['DailyForecasts'][day]['Day']['IconPhrase']
        night_forecast = forecast_data['DailyForecasts'][day]['Night']['IconPhrase']
        five_day.append([temp_max, temp_min, day_forecast, night_forecast])

    return five_day

if __name__ == "__main__":
application.run(debug=True)