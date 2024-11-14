from SpotifyRecommender import SpotifyRecommender
from LLM_Jose import LLM

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
        genre_seeds = genres
        artist_seeds = [self.sp.search_artist_id(artist) for artist in artists if self.sp.search_artist_id(artist)]
        track_seeds = [self.sp.search_track_id(song) for song in songs if self.sp.search_track_id(song)]
        recommendations = self.sp.get_track_recommendations(track_seeds=track_seeds, 
                                                            artist_seeds=artist_seeds, 
                                                            genre_seeds=genre_seeds, 
                                                            mood=mood,
                                                            spotify_data=spotify_data)
        #print('Recommendation: ', recommendations)
        sample_list_Jose = [self.sp.get_track_sample(song_name) for song_name, _ in recommendations]
        #print(sample_list_Jose)
        return self.llm.give_user_recommendations(songs_list = recommendations, song_previews=sample_list_Jose)