
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class LLM:
    
    openai_api_token : str
    user_name : str = 'User'
    user_request_prediction : str = ''
    
    #Templates
    #Example song description : 'Upbeat music to dance along'
    
    greet_template = PromptTemplate(
        input_variables=['user_name'],
        template="""Greet a user called: {user_name} in a friendly but professional way.
                In this context you are a web application that is going to recommend music to the user.
                Make the response original to each user. Respond with only one line."""
    )

    spotify_data_template = PromptTemplate(
        input_variables=['description'],
        template='''
These are the parameters needed for the Spotify Recommendations API. Some key parameters include:
    acousticness: A measure of whether the track is acoustic (value range: 0.0 - 1.0).
    danceability: How suitable the track is for dancing, based on tempo, rhythm stability, etc. (value range: 0.0 - 1.0).
    energy: A measure of intensity and activity (value range: 0.0 - 1.0).
    instrumentalness: The likelihood that the track is instrumental (value range: 0.0 - 1.0).
    liveness: A measure of the presence of a live audience (value range: 0.0 - 1.0).
    valence: A measure of the musical positiveness conveyed by the track (value range: 0.0 - 1.0).
    tempo: The tempo of the track in beats per minute (integer, typical range: 60-200 BPM).
    speechiness: A measure of the presence of spoken words (value range: 0.0 - 1.0).

According to the user's description of the music they would like to listen to: {description}. 
If the description does not provide specific details, assume reasonable values based on common music preferences. Always respond in this exact format:

acousticness: [value]
danceability: [value]
energy: [value]
instrumentalness: [value]
liveness: [value]
valence: [value]
tempo: [value]
speechiness: [value]

Do not request clarification, and do not include explanations in your response.
'''
    )
    
    recommend_podcast_template = PromptTemplate(
        input_variables=['description'],
        template=''' In this context you are "Songs 4Geeks", a music recommendation app which can also recommend podcasts.
        According to this description: {description}.Please recommend a podcast that matches said description to the user.
        Please restrict your response to 145 tokens. Please do not greet the user. Please respond only with a list of podcast
        names. Please make sure the podcast exists on Spotify.
        
        '''
    )
    
    custom_recommendation_template = PromptTemplate(
        input_variables=['user_name', 'description', 'song_list'],
        template='''The user's name is: {user_name}. Please let the user know, in a professional and friendly way, that you have a list of songs
        that you would like to recommend to them. In this context you are a web application called Songs 4-Geeks that is going to recommend music to the user. 
        Take into account this list of songs that were recommended to the user: {song_list}. Please also explain to the user why you chose those songs based on
        their request: {description}. Please don't focus too much on specific songs and more on the overall description. Please keep your response as short as 200 tokens,
        with a small 10 tokens margin to finish the idea in an organic way. Please do not greet the user.
        
        '''
    )
#Constructor method
    def __init__(self, openai_key : str) -> None:
        self.openai_api_token = openai_key
        
#Required for custom greetings to the user
    def set_username(self, user_name : str) -> None:
        self.user_name = user_name
    
#Used by all prompt methods (greet_user, get_spotify_recommendation_data, give_user_recommendations)
    def prompt_llm(self, prompt_variable, prompt_template: PromptTemplate) -> str:
        # Initialize the LLM
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, max_tokens=250, api_key=self.openai_api_token)
        
        # Create the chain using the prompt template
        chain = prompt_template | llm

        # Handle `prompt_variables` as str or list of strings
        if isinstance(prompt_variable, str):
            # If `prompt_variable` is a string, assume it corresponds to the first input variable
            response = chain.invoke({prompt_template.input_variables[0]: prompt_variable})
        elif isinstance(prompt_variable, list) and all(isinstance(item, str) for item in prompt_variable):
            # If `prompt_variable` is a list of strings, map them to `input_variables`
            if len(prompt_template.input_variables) != len(prompt_variable):
                raise ValueError("Number of prompt variables does not match the number of input variables in the template.")
            # Create a dictionary matching input_variables with the list values
            input_dict = dict(zip(prompt_template.input_variables, prompt_variable))
            print('Input variables: ', input_dict)
            response = chain.invoke(input_dict)
        else:
            # Raise an error for unsupported `prompt_variables` types
            raise TypeError("`prompt_variables` must be a str or a list of strings.")
        
        # Return the content if the response is of type AIMessage, otherwise return the response directly
        return response.content if hasattr(response, 'content') else response


#Parses the LLMs response into a dictionary of values
    def parse_model_output_to_dict(self, model_output) -> dict:
        fallback_values = {
            "acousticness": 0.5,
            "danceability": 0.5,
            "energy": 0.5,
            "instrumentalness": 0.5,
            "liveness": 0.2,
            "valence": 0.5,
            "tempo": 120,
            "speechiness": 0.1,
        }
        try :
            print('parsing model output')
            print(model_output)
            # Extract the content from the AIMessage object
            content = model_output.content if hasattr(model_output, 'content') else model_output
            print('COntent: ', content)
            # Split the model output into lines
            output_lines = content.strip().splitlines()
            print('output lines: ', output_lines)
            # Initialize an empty dictionary to store the results
            result_dict = {}
            
            # Loop through each line, split by ':' and add the result to the dictionary
            for line in output_lines:
                print('every line: ', line)
                key, value = line.split(':')
                result_dict[key.strip()] = float(value.strip())  # Convert the value to float if it's a numeric value
            return result_dict
        except Exception as e:
            return fallback_values
    
    ########Prompt functions##########
    #Returns text greeting the user according to its username. Must call set_username({user's_name}) first
    def greet_user(self) -> str:
        model_response = self.prompt_llm( prompt_variable = self.user_name, prompt_template = self.greet_template)
        return model_response
    
    #Returns a pandas DataFrame containing the additional values needed for a custon Spotify API Recommendations call.
    #The values are listed under the recommendation_template.
    def get_spotify_recommendation_data(self, user_input : str) -> dict:
        self.user_request_prediction = user_input
        model_output = self.prompt_llm( prompt_variable=self.user_request_prediction, prompt_template=self.spotify_data_template)
        print('model output: ', model_output)
        return self.parse_model_output_to_dict(model_output=model_output)
    
    def get_spotify_podcast_list(self, user_input : str) -> dict:
        model_output = self.prompt_llm( prompt_variable=user_input, prompt_template=self.recommend_podcast_template)
        return model_output
    
    #Given a list of song names, this method returns a custom message for the user with his requested recommendations.
    def give_user_recommendations(self, songs_list : list[tuple], song_previews : list[str] = None) -> str:
        prompt_song_list = ', '.join([song[0] + ' by ' + song[1] for song in songs_list])
        model_output = self.prompt_llm( prompt_variable=[prompt_song_list, self.user_request_prediction, self.user_name], prompt_template=self.custom_recommendation_template)
        response = model_output
        print(response)
        combined_song_list = [(song[0], song[1], song_previews[i] if i < len(song_previews) else None) for i, song in enumerate(songs_list)]  
        
        return response, combined_song_list
    
   