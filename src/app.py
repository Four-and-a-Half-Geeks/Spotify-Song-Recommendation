from flask import Flask, request, render_template, session
from pickle import load
import regex as re
import os
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
#from apikey import apikey
from SpotifyAPI import SpotifyAPI
#from LLM import LLM
from dotenv import load_dotenv
from SpotifyCarlos import SpotifyCarlos
from Backend import Backend
from LLM_Jose import LLM

#os.environ["OPENAI_API_KEY"] = apikey

#website link https://ml-web-app-using-flask-e8bg.onrender.com/


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
    user_greeting = "Welcome!"

    #def load_env():
        #"""Load environment variables from a .env file."""
        #env_file_path = '.env'
        #try:
            #with open(env_file_path) as f:
                #for line in f:
                    # Remove whitespace and skip comments
                    #line = line.strip()
                    #if line and not line.startswith('#'):
                        #key, value = line.split('=', 1)
                        #os.environ[key.strip()] = value.strip()  # Strip whitespace from both key and value
                        #print(f"Loaded '{key.strip()}' = '{value.strip()}'")
        #except FileNotFoundError:
            #print(f"Warning: {env_file_path} file not found.")

    
    #load_env()
    try:
        load_dotenv()
        
        huggingface_key = os.getenv('HUGGING_FACE_TOKEN')

        if not huggingface_key:
            print("Error: Token not found.")
            return
        llm = LLM(openai_key)
        llm.set_username(user_name=user_name)
        print(llm.greet_user())
        user_greeting = llm.greet_user()
        
        #WARNING: When running the app, a lot of Langchain warnings appear in the chat. They are harmless.

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
            print("genres in else")
            print(genres)
        #genres = [genre.lower() for genre in request.form.getlist("genres")]
        #artists = []
        #songs = []

        # Load environment variables and check for keys
        load_dotenv()
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        huggingface_key = os.getenv('HUGGING_FACE_TOKEN')
        #openai_key = os.getenv("OPENAI_KEY_JOSE")

        if not client_id or not client_secret or not huggingface_key:
            print("Error: Client ID and/or Client Secret not found.")
            return render_template("error.html", message="Spotify or Hugging Face credentials not found.")
        
        # Initialize Spotify and LLM classes
        #sp = SpotifyAPI(client_id, client_secret)
        #llm = LLM(huggingface_key)

        

        # Get Spotify data and recommendations
        #spotify_data = llm.get_spotify_recommendation_data(user_input=recommendation_request)


        #start of carlos code----------------------------------------------------
        #recommender = SpotifyCarlos(client_id, client_secret)
        #recommendations_Carlos = recommender.get_track_recommendations(genre_seeds=genres, spotify_data=spotify_data)
        #sample_list_Carlos = [sp.get_track_sample(song_name) for song_name in recommendations_Carlos]
        #recommendations_Carlos_enumerated = [(idx + 1, track_name, artist_name) for idx, (track_name, artist_name) in enumerate(recommendations_Carlos)]
        #print(recommendations_Carlos_enumerated)
        #recommendations_Carlos_enumerated = [
        #(*rec, sample_list_Carlos[idx]) for idx, rec in enumerate(recommendations_Carlos_enumerated)
        #]
        #print(recommendations_Carlos_enumerated)
        #if recommendations_Carlos:
            #print("\nRecommended Songs:")
            #print(genres)
            #for idx, (track_name, artist_name) in enumerate(recommendations_Carlos, start=1):
                #print(f"{idx}. {track_name} by {artist_name}")
        #else:
            #print("No recommendations available. Try using different input options.")
        #end of carlos code------------------------------------------------------

        #start of Jose's code----------------------------------------------------
        backend = Backend(client_id, client_secret, openai_key)
        sp = SpotifyAPI(client_id, client_secret)
        greeting = backend.get_user_greeting(user_name)
        #print(greeting)
        llm = LLM(openai_key)
        spotify_data = llm.get_spotify_recommendation_data(user_input=recommendation_request)
        #print(spotify_data)
        greeting_Jose, recommendations_Jose = backend.get_user_recommendation(genres, artists, songs, None, spotify_data)
        #print(greeting_Jose)
        #sample_list_Jose = [sp.get_track_sample(song_name) for song_name, _ in recommendations_Jose]
        #print(sample_list_Jose)

        #end of Jose's code------------------------------------------------------

        
        #recommendations = sp.get_track_recommendations(genre_seeds=genres, amount=10, spotify_data=spotify_data)
        #sample_list = [sp.get_track_sample(song_name) for song_name in recommendations]

        # Generate a recommendation list as a single string
        #if recommendations:
            #recommendation_string = llm.give_user_recommendations(song_names_list=recommendations, song_previews=sample_list)
            # Split by lines to get individual recommendations
            #recommendation_list = recommendation_string.strip().split('\n')
        #else:
            #recommendation_list = ["No recommendations found."]

    except Exception as e:
        print("An error occurred:", e)
    
    return render_template("recommendation_list.html", user_name = user_name, list = recommendations_Jose, greeting = greeting_Jose)


if __name__ == "__main__":
    # Use the port provided by Render, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Set host to 0.0.0.0 to be accessible externally
    app.run(host="0.0.0.0", port=port, debug=True)

#     from flask import Flask, request, jsonify

# app = Flask(__name__)

# # Sample list of strings
# data = ["apple", "apricot", "banana", "blueberry", "blackberry", "cherry", "date", "dragonfruit"]

# @app.route('/autocomplete', methods=['GET'])
# def autocomplete():
#     query = request.args.get('query', '').lower()
#     if query:
#         # Filter data based on query
#         suggestions = [item for item in data if query in item.lower()]
#     else:
#         suggestions = []
    
#     # Return as JSON response
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <title>Autocomplete Example</title>
# </head>
# <body>
#     <input type="text" id="searchBox" placeholder="Type to search...">
#     <ul id="suggestions"></ul>

#     <script>
#         const searchBox = document.getElementById('searchBox');
#         const suggestionsList = document.getElementById('suggestions');

#         searchBox.addEventListener('input', function() {
#             const query = searchBox.value;
#             fetch(`/autoc
# Jose Alejandro Sosa Nuñez
# 4:17 PM
# searchBox.addEventListener('input', function() {
#             const query = searchBox.value;
#             fetch(`/autocomplete?query=${query}`)
#                 .then(response => response.json())
#                 .then(data => {
#                     suggestionsList.innerHTML = '';
#                     data.suggestions.forEach(item => {
#                         const listItem = document.createElement('li');
#                         listItem.textContent = item;
#                         suggestionsList.appe
# suggestionsList.appendChild(listItem);
#                     });
#                 });
#         });
#     </script>
# </body>
# </html>

#To play a preview from a Spotify preview_url, you can use the HTML <audio> element or JavaScript. Here’s how to set it up in a webpage: <audio controls>
   #<source src="YOUR_PREVIEW_URL_HERE" type="audio/mpeg">
    #Your browser does not support the audio element.
#</audio>