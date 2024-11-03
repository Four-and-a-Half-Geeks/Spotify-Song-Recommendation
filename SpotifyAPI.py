import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI:
    
    sp : spotipy.Spotify
    
    def __init__(self, client_id, secret_id):
        auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=secret_id)
        self.sp = spotipy.Spotify(auth_manager=auth_manager)
        
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
        
    #For autocompletion
    def get_all_genre_seed(self, genre_name : str) -> list:
        genre_seeds = self.sp.recommendation_genre_seeds()
        return genre_seeds['genres']
    
    def get_track_recommendations(self, track_seeds : list[str] = None,\
        artist_seeds : list[str] = None,genre_seeds : list[str] = None, amount : int = '20', country : str = 'US') -> list:
        if not (track_seeds or artist_seeds or genre_seeds):
            raise ValueError("At least one of seed_tracks, seed_artists, or seed_genres must be provided.")

        # Prepare the input parameters for the Spotify API
        try:
            recommendations = self.sp.recommendations(
                seed_tracks=track_seeds,
                seed_artists=artist_seeds,
                seed_genres=genre_seeds,
                limit=amount,
                country=country
            )
            return [track['name'] for track in recommendations['tracks']]
        except spotipy.SpotifyException as e:
            print(f"Error: {e}")
            return None