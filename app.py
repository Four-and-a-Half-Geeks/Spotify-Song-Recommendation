import os
from SpotifyAPI import SpotifyAPI
from LLM import LLM

def load_env():
    """Load environment variables from a .env file."""
    env_file_path = '.env'
    try:
        with open(env_file_path) as f:
            for line in f:
                # Remove whitespace and skip comments
                line = line.strip()
                if line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()  # Strip whitespace from both key and value
                    print(f"Loaded '{key.strip()}' = '{value.strip()}'")
    except FileNotFoundError:
        print(f"Warning: {env_file_path} file not found.")

def main():
    load_env()
    try:
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        huggingface_key = os.getenv('HUGGING_FACE_TOKEN')

        if not client_id or not client_secret or not huggingface_key:
            print("Error: Client ID and/or Client Secret not found.")
            return

        sp = SpotifyAPI(client_id, client_secret)
        llm = LLM(huggingface_key)
        user_name = 'Johnny'
        llm.set_username(user_name=user_name)
        print(llm.greet_user())
        user_input = 'Upbeat music to dance along'
        spotify_data = llm.get_spotify_recommendation_data(user_input=user_input)
        recommendations = sp.get_track_recommendations(genre_seeds=['jazz'], amount=10, spotify_data=spotify_data)
        sample_list : list = []
        for song_name in recommendations:
            sample_list.append(sp.get_track_sample(song_name))
        
        #WARNING: When running the app, a lot of Langchain warnings appear in the chat. They are harmless.
        if recommendations:
            #print("Track Recommendations:", recommendations)
            print(llm.give_user_recommendations(song_names_list = recommendations,song_previews= sample_list))
        else:
            print("No recommendations found.")

    except Exception as e:
        print("An error occurred:", e)

# Run the main function if this file is executed as a script
if __name__ == "__main__":
    main()
    
    
    
#Results:
# Johnny,

# We have a list of songs that we think you'll enjoy. Please let us know if you'd like us to play any of them.
# ```Blessed Are the Bleak preview url: https://p.scdn.co/mp3-preview/a53ae8ca6445f18b769ffb086bb01dc2cc553fcf?cid=442602d418c546d78a8e65ce8b3c3d78
# Little Black Train preview url: https://p.scdn.co/mp3-preview/751cd3ec2ee5cd64f14115f6378cc405a1d0d8f1?cid=442602d418c546d78a8e65ce8b3c3d78
# Stellar Regions (Venus)
# Like Someone In Love preview url: https://p.scdn.co/mp3-preview/1a39b5f372de737c38c211df597f1c982f0e565c?cid=442602d418c546d78a8e65ce8b3c3d78
# I've Got You Under My Skin - Remastered 1998
# I Let a Song Go out of My Heart preview url: https://p.scdn.co/mp3-preview/e6836a978b360ed127ecdaead051aada11189042?cid=442602d418c546d78a8e65ce8b3c3d78
# My Girl
# Cuando Cuando
# Cantaloupe Island
# You Make Me Feel so Young
