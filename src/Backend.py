from SpotifyRecommender import SpotifyRecommender
from LLM import LLM

class Backend:
    
    sp : SpotifyRecommender
    llm : LLM
    
    def __init__(self, client_id : str, client_secret : str, huggingface_key : str):
        self.llm = LLM(huggingface_key)
        self.sp = SpotifyRecommender(client_id, client_secret)
        
    def get_user_greeting(self, _user_name : str) -> str:
        self.llm.set_username(user_name=_user_name)
        return self.llm.greet_user()
    
    def get_user_recommendation(self, genres : list[str], artists : list[str], songs : list[str], mood : str, spotify_data) -> str:
        print("Get user recommendations :", genres, artists, songs, spotify_data)
        #The recommendation cannot contain more than 5 of genres, songs, artists
        if (len(genres) + len(songs) + len(artists)) > 5:
            while len(genres) > 3 and (len(genres) + len(songs) + len(artists)) > 5:
                print('Genre length: ', len(genres))
                genres.pop()
            while len(songs) > 1 and (len(genres) + len(songs) + len(artists)) > 5:
                print('Genre length: ', len(songs))
                songs.pop()
            while len(artists) > 1 and (len(genres) + len(songs) + len(artists)) > 5:
                print('Genre length: ', len(artists))
                artists.pop()
        print("Get user recommendations AFTER:", genres, artists, songs, spotify_data)
        
        genre_seeds = genres
        artist_seeds = [self.sp.search_artist_id(artist) for artist in artists if self.sp.search_artist_id(artist)]
        track_seeds = [self.sp.search_track_id(song) for song in songs if self.sp.search_track_id(song)]

        recommendations = self.sp.get_track_recommendations(track_seeds=track_seeds, 
                                                            artist_seeds=artist_seeds, 
                                                            genre_seeds=genre_seeds, 
                                                            mood=mood,
                                                            spotify_data=spotify_data)
        print('Recommendation: ', recommendations)
        sample_list = [self.sp.get_track_sample(song_name) for song_name, _ in recommendations]
        return self.llm.give_user_recommendations(songs_list = recommendations, song_previews=sample_list)