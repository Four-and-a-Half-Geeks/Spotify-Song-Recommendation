import os
from SpotifyAPI import SpotifyAPI

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
    print(os.getenv('SPOTIFY_CLIENT_ID'))
    print(os.getenv('SPOTIFY_CLIENT_SECRET'))
    try:
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

        if not client_id or not client_secret:
            print("Error: Client ID and/or Client Secret not found.")
            return

        sp = SpotifyAPI(client_id, client_secret)
        recommendations = sp.get_track_recommendations(genre_seeds=['classical', 'country'])
        
        if recommendations:
            print("Track Recommendations:", recommendations)
            print(sp.get_track_sample(recommendations[0]))
        else:
            print("No recommendations found.")

    except Exception as e:
        print("An error occurred:", e)

# Run the main function if this file is executed as a script
if __name__ == "__main__":
    main()
    
    
    
#Results:
 #   Track Recommendations: ['The House That Built Me', 'Achorripsis',
 # 'Capriccio Espagnol, Op. 34: I. Alborada', 'Follow That Dust',
 # 'Tchaikovsky: Swan Lake, Op. 20, Act II: No. 13d, Dance of the Swans.
 # Dance of the Little Swans', 'Rumor', 'Find out Who Your Friends Are',
 # 'Summer Cool', 'Drunk On A Plane', 'Rearview Town', 'Sonate pour clarinette et piano H.42: II. Lent et soutenu',
 # 'The Race Is On', 'Plus Que Ma Prope Vie', 'Symphony No. 3 in E-Flat Major, Op. 55 "Eroica": I. Allegro con brio',
 # 'One That Got Away', 'California', "Thinkin' Problem", 'Leave My Head Alone Brain Seven',
 # 'Fantasia on a Theme by Thomas Tallis', 'Only Questions']
