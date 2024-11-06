import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI:
    
    sp : spotipy.Spotify
    
    #Constructor. Takes SpotifyAPI credentials.
    def __init__(self, client_id, secret_id):
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret_id)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
    #The get seed methods are useful to get the seed code from a name in the case of tracks and artists.
    #Also for checking if the genre name provided is available in the Spotify API.
    def get_track_seed(self, track_name : str) -> str:
        if not track_name:
            return ''
        else:
            result = self.sp.search(q=track_name, type='track', limit=1)
            if result['tracks']['items']:
                track_id = result['tracks']['items'][0]['id']
                return track_id
            else:
                return "Track not found."
        
    def get_artist_seed(self, artist_name: str) -> str:
        if not artist_name:
            return ''
        else:
            result = self.sp.search(q=artist_name, type='artist', limit=1)
            if result['artists']['items']:
                artist_id = result['artists']['items'][0]['id']
                return artist_id
            else:
                return "Artist not found."
            
    def get_genre_seed(self, genre_name : str) -> str:
        genre_seeds = self.sp.recommendation_genre_seeds()
        if genre_name in genre_seeds:
            return genre_name
        else:
            return 'Genre not found'
        
    #For autocompletion of the genre input field. May improve user experience
    def get_all_genre_seed(self, genre_name : str) -> list:
        genre_seeds = self.sp.recommendation_genre_seeds()
        return genre_seeds['genres']
    
    #Main method for getting recommendations. Returns a list of names (strings) for all songs.
    def get_track_recommendations(self, track_seeds : list[str] = None,\
        artist_seeds : list[str] = None,genre_seeds : list[str] = None, \
            amount : int = '20', country : str = 'US', spotify_data : dict = None) -> list:
        if not (track_seeds or artist_seeds or genre_seeds):
            raise ValueError("At least one of seed_tracks, seed_artists, or seed_genres must be provided.")

        # Prepare the input parameters for the Spotify API
        try:
            recommendations = self.sp.recommendations(
                seed_tracks=track_seeds,
                seed_artists=artist_seeds,
                seed_genres=genre_seeds,
                limit=amount,
                country=country,
                target_acousticness=spotify_data.get('acousticness', 0.5) if spotify_data else 0.5,
                target_danceability=spotify_data.get('danceability', 0.5) if spotify_data else 0.5,
                target_duration_ms=int(210000) if spotify_data else 210000,  # Replace with an integer
                target_energy=spotify_data.get('energy', 0.5) if spotify_data else 0.5,
                target_instrumentalness=spotify_data.get('instrumentalness', 0.0) if spotify_data else 0.0,
                target_speechiness=spotify_data.get('speechiness', 0.5) if spotify_data else 0.5,
                target_tempo=spotify_data.get('tempo', 120.0) if spotify_data else 120.0,
                target_valence=spotify_data.get('valence', 0.5) if spotify_data else 0.5
            )
            return [track['name'] for track in recommendations['tracks']]
        except spotipy.SpotifyException as e:
            print(f"Error: {e}")
            return None
        
    #Returns the url of the song preview, which is an MP3 file of 30 second duration.
    def get_track_sample(self, track_name : str) -> str:
        track_id = self.get_track_seed(track_name)
        try:
            # Fetch track details from Spotify
            track = self.sp.track(track_id)
            
            # Extract the preview URL if available
            preview_url = track.get('preview_url')
            if preview_url:
                print(f"Preview URL for track {track_id}: {preview_url}")
                return preview_url
            else:
                print(f"No preview available for track {track_id}.")
                return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None