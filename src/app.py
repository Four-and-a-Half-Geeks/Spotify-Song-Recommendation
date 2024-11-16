from flask import Flask, request, render_template, session
from pickle import load
import regex as re
import os
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from dotenv import load_dotenv
from Backend import Backend

# Define the Flask app and set the template folder path
app = Flask(__name__, template_folder='../templates')
app.secret_key = '1'

#class_dict = {
   # "1": "POSITIVE",
   # "0": "NEGATIVE"
#}

# Ensure wordnet and stopwords are downloaded once
download("wordnet")
download("stopwords")
stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()
backend : Backend
load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

@app.route("/", methods=["GET", "POST"])
def index():

    # Render the template with the prediction result (or None if GET request)
    return render_template("index.html")

@app.route("/recommendation", methods=["POST"])
def recommendation():
    # Get the input value
    user_name = str(request.form["user_name"])
    openai_key = str(request.form["AI_APIKEY"])
    session['user_name'] = user_name
    session['openai_key'] = openai_key

    try:
        load_dotenv()
        
        backend = Backend(client_id, client_secret, openai_key)
        user_greeting = backend.get_user_greeting(user_name)

    except Exception as e:
        print("An error occurred:", e)

    # Render a new page with the prediction result
    return render_template("recommendation.html", user_greeting = user_greeting)

@app.route("/recommendation_list", methods=["POST"])
def recommendation_list():
    try:
        user_name = session.get('user_name', 'Guest')
        openai_key = session.get('openai_key', 'Guest')
        recommendation_request = str(request.form["recommendation_request"])
        genres = str(request.form["genres"]).lower().split(',')
        artists = str(request.form["artist_names"]).lower().split(',')
        songs = str(request.form["song_names"]).lower().split(',')
        
        print("here are the artist names")
        print(artists)

        print("here are the songs")
        print(songs)
        
        print("here are the typed in genres")
        print(genres)
        
        selected_genres = request.form.getlist("genre")

        print("here are the genres from the checkbox")
        print(selected_genres)

        genres.extend(selected_genres)
        print("here are the combined genres")
        print(genres)
        
        #NEEDS AT LEAST GENRES OR ARTIST OR SONG SEEDS OR SPOTIFYRECOMMENDER.PY THROWS AN ERROR

        if genres == ['']:
            genres = []
            print("I'm in the if")
        else:
            print(genres)
            genres = [genre.strip() for genre in genres]

        # Load environment variables and check for keys
        load_dotenv()
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        backend = Backend(client_id, client_secret, openai_key)
        
        greeting = backend.get_user_greeting(user_name)
        
        spotify_data = backend.llm.get_spotify_recommendation_data(user_input=recommendation_request)
        
        greeting, recommendations = backend.get_user_recommendation(genres, artists, songs, None, spotify_data)
        print('Recommendations: ', recommendations)

    except Exception as e:
        print("An error occurred:", e)
    
    return render_template("recommendation_list.html", user_name = user_name, list = recommendations, greeting = greeting)


if __name__ == "__main__":
    # Use the port provided by Render, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Set host to 0.0.0.0 to be accessible externally
    app.run(host="0.0.0.0", port=port, debug=True)