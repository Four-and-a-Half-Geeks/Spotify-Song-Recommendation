from flask import Flask, request, render_template, session
import os
from dotenv import load_dotenv
from Backend import Backend

# Define the Flask app and set the template folder path
app = Flask(__name__, template_folder='../templates', static_folder='../static')
app.secret_key = '1'

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
        
        selected_genres = request.form.getlist("genre")

        genres.extend(selected_genres)
        
        #NEEDS AT LEAST GENRES OR ARTIST OR SONG SEEDS OR SPOTIFYRECOMMENDER.PY THROWS AN ERROR

        if genres == ['']:
            genres = []
        else:
            genres = [genre.strip() for genre in genres]

        # Load environment variables and check for keys
        load_dotenv()
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        backend = Backend(client_id, client_secret, openai_key)
        
        greeting = backend.get_user_greeting(user_name)
        
        spotify_data = backend.llm.get_spotify_recommendation_data(user_input=recommendation_request)
        
        greeting, recommendations = backend.get_user_recommendation(genres, artists, songs, None, spotify_data)

    except Exception as e:
        print("An error occurred:", e)
    
    print('!!!!!!user_name: ', user_name)
    print('!!!!!!!!recommendations: ', recommendations)
    print('!!!!!!!!greeting: ', greeting)
    
    return render_template("recommendation_list.html", user_name = user_name, list = recommendations, greeting = greeting)


if __name__ == "__main__":
    # Use the port provided by Render, or default to 5000
    port = int(os.environ.get("PORT", 8080))
    # Set host to 0.0.0.0 to be accessible externally
    app.run(host="0.0.0.0", port=port, debug=True)