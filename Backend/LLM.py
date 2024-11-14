
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

class LLM:
    
    openai_api_token : str
    user_name : str = 'User'

    #Using templates for custom prompts
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
    acousticness: A measure of whether the track is acoustic.
    danceability: How suitable the track is for dancing, based on tempo, rhythm stability, etc.
    energy: A measure of intensity and activity (e.g., fast, loud, or agitated music).
    instrumentalness: The likelihood that the track is instrumental.
    liveness: A measure of the presence of a live audience.
    valence: A measure of the musical positiveness conveyed by the track (e.g., happy vs. sad).
    tempo: The tempo of the track in beats per minute.
    speechiness: A measure of the presence of spoken words.
According to the user's description of the music they would like to listen to: {description}. 
Please provide values for all fields above. Respond only with said values.
'''
    )
    
    custom_recommendation_template = PromptTemplate(
        input_variables=['user_name'],
        template='''The user's name is: {user_name}. Please let the user know, in a professional and friendly way, that you have a list of songs
        that you would like to recommend to them. In this context you are a web application that is going to recommend music to the user. Please limit your response to a single line of text.
        
        '''
    )
#Constructor method
    def __init__(self, openai_key : str) -> None:
        self.openai_api_token = openai_key
        
#Required for custom greetings to the user
    def set_username(self, user_name : str) -> None:
        self.user_name = user_name
    
#Used by all prompt methods (greet_user, get_spotify_recommendation_data, give_user_recommendations)
    def prompt_llm(self, prompt_variable : str, prompt_template : PromptTemplate = None) -> str:
        llm = ChatOpenAI(model_name="gpt-4", temperature=0.7, max_tokens=150, api_key=self.openai_api_token)
        chain = prompt_template | llm
        input_variable_name = prompt_template.input_variables[0]
        if prompt_template:
            response = chain.invoke({input_variable_name: prompt_variable})
        else:
            response = llm(prompt_variable)
        #If the response is of type AIMessage, return only the content
        return response.content if hasattr(response, 'content') else response

#Parses the LLMs response into a dictionary of values
    def parse_model_output_to_dict(self, model_output) -> dict:
        # Extract the content from the AIMessage object
        content = model_output.content if hasattr(model_output, 'content') else model_output
        
        # Split the model output into lines
        output_lines = content.strip().splitlines()
        
        # Initialize an empty dictionary to store the results
        result_dict = {}
        
        # Loop through each line, split by ':' and add the result to the dictionary
        for line in output_lines:
            key, value = line.split(':')
            result_dict[key.strip()] = float(value.strip())  # Convert the value to float if it's a numeric value

        return result_dict
    
    ########Pormpt functions##########
    #Returns text greeting the user according to its username. Must call set_username({user's_name}) first
    def greet_user(self) -> str:
        model_response = self.prompt_llm( prompt_variable = self.user_name, prompt_template = self.greet_template)
        return model_response
    
    #Returns a pandas DataFrame containing the additional values needed for a custon Spotify API Recommendations call.
    #The values are listed under the recommendation_template.
    def get_spotify_recommendation_data(self, user_input : str) -> pd.DataFrame:
        model_output = self.prompt_llm( prompt_variable=user_input, prompt_template=self.spotify_data_template)
        return self.parse_model_output_to_dict(model_output=model_output)
    
    #Given a list of song names, this method returns a custom message for the user with his requested recommendations.
    def give_user_recommendations(self, songs_list : list[tuple], song_previews : list[str] = None) -> str:
        
        model_output = self.prompt_llm( prompt_variable=self.user_name, prompt_template=self.custom_recommendation_template)
        response = model_output
        response += '\n'
        i = 0
        for song_data in songs_list:
            response += '\n'        
            response += song_data[0] + ' by ' + song_data[1]
            if song_previews and song_previews[i] != None:
                response += ' preview url: ' + song_previews[i]
            i += 1   
        
        return response
    
   