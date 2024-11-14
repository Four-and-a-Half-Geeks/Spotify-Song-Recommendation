import os
import pandas as pd
import numpy as np
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException
import matplotlib.pyplot as plt
import random

class SpotifyCarlos:

    sp : spotipy.Spotify

    def __init__(self, client_id, secret_id):
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret_id)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def get_available_genres(self):
        """Retrieve available genre seeds from Spotify."""
        return self.sp.recommendation_genre_seeds()['genres']

    def search_artist_id(self, artist_name):
        """Search for an artist and return their Spotify ID."""
        result = self.sp.search(q='artist:' + artist_name, type='artist', limit=1)
        if result['artists']['items']:
            return result['artists']['items'][0]['id']
        print(f"Warning: No artist found for '{artist_name}'")
        return None

    def search_track_id(self, track_name):
        """Search for a track and return its Spotify ID."""
        result = self.sp.search(q='track:' + track_name, type='track', limit=1)
        if result['tracks']['items']:
            return result['tracks']['items'][0]['id']
        print(f"Warning: No track found for '{track_name}'")
        return None
    # Main method for getting recommendations
    def get_track_recommendations(self, track_seeds=None, artist_seeds=None, genre_seeds=None, 
                                  amount=20, country="US", mood=None, spotify_data = None):
        if not (track_seeds or artist_seeds or genre_seeds):
            raise ValueError("At least one of seed_tracks, seed_artists, or seed_genres must be provided.")
        
        # Convert genre seeds to lowercase and filter based on available genres
        available_genres = self.get_available_genres()
        genre_seeds = [genre.lower() for genre in genre_seeds if genre.lower() in available_genres]
        
        # Set default Spotify audio feature values
        spotify_data = {
            'acousticness': 0.5,
            'danceability': 0.5,
            'duration_ms': 210000,
            'energy': 0.5,
            'instrumentalness': 0.0,
            'speechiness': 0.5,
            'tempo': 120.0,
            'valence': 0.5
        }
        
        # Define mood parameters
        mood_map = {
            'happy': {'valence': 0.8, 'danceability': 0.7},
            'sad': {'valence': 0.2, 'acousticness': 0.7},
            'dance': {'danceability': 0.9, 'energy': 0.8},
            'relaxed': {'valence': 0.6, 'acousticness': 0.8, 'energy': 0.3, 'tempo': 80.0},
            'energetic': {'energy': 0.9, 'danceability': 0.8, 'tempo': 140.0},
            'romantic': {'valence': 0.7, 'acousticness': 0.6, 'energy': 0.4},
            'calm': {'valence': 0.4, 'acousticness': 0.9, 'energy': 0.2, 'tempo': 60.0},
            'angry': {'energy': 0.8, 'valence': 0.2, 'danceability': 0.5, 'tempo': 150.0},
            'focus': {'acousticness': 0.6, 'instrumentalness': 0.5, 'tempo': 100.0},
            'uplifting': {'valence': 0.9, 'energy': 0.7, 'danceability': 0.6, 'tempo': 120.0}
        }
        
        # Apply mood-based filtering if valid mood is provided
        if mood and mood.lower() in mood_map:
            spotify_data.update(mood_map[mood.lower()])
        elif mood:
            print(f"Invalid mood '{mood}' provided. Skipping mood-based filtering.")

        # Prepare the input parameters for the Spotify API
        try:
            recommendations = self.sp.recommendations(
                seed_tracks=track_seeds,
                seed_artists=artist_seeds,
                seed_genres=genre_seeds,
                limit=amount,
                country=country,
                #spotify_data = spotify_data
                target_acousticness=spotify_data.get('acousticness', 0.5),
                target_danceability=spotify_data.get('danceability', 0.5),
                target_duration_ms=int(spotify_data.get('duration_ms', 210000)),
                target_energy=spotify_data.get('energy', 0.5),
                target_instrumentalness=spotify_data.get('instrumentalness', 0.0),
                target_speechiness=spotify_data.get('speechiness', 0.5),
                target_tempo=spotify_data.get('tempo', 120.0),
                target_valence=spotify_data.get('valence', 0.5)
            )
            # Return only track names as per requirements
            return [(track['name'], track['artists'][0]['name']) for track in recommendations['tracks']]
        except SpotifyException as e:
            print(f"Error: {e}")
            return None
