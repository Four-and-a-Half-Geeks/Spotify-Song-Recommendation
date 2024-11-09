
from langchain.llms import HuggingFaceHub
import pandas as pd
import re
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

class LLM:
    
    huggingface_api_token = os.getenv('HUGGING_FACE_TOKEN')
    user_name : str = 'User'
    
    #Templates
    #song_description = 'Upbeat music to dance along'
    
    greet_template = PromptTemplate(
        input_variables=['user_name'],
        template='''Greet a user called: {user_name} in a friendly but professional way.
                                                Please limit your response to a single line of text.
                                                In this context you are a web application that is going to recommend music to the user.
                                                Make the response a little bit different every time.'''
    )
    
    song_template = PromptTemplate(
        input_variables=['description'],
        template='Recommend me a song that matches this description: {song_description}.\
            Include in your response only the name of the song, and only one song.'
    )

    spotify_data_template = PromptTemplate(
        input_variables=['user_input'],
        template='''Given the song description: {user_input}.

Provide specific numeric values for the following Spotify API parameters without any extra text:

acousticness: 
danceability: 
duration: 
energy: 
instrumentalness: 
key: 
popularity: 
speechiness: 
tempo: 
valence: '''
    )
    
    custom_recommendation_template = PromptTemplate(
        input_variables=['user_name'],
        template='''The user's name is: {user_name}. Please let the user know, in a professional and friendly way, that you have a list of songs
        that you would like to recommend to them. In this context you are a web application that is going to recommend music to the user. Please limit your response to a single line of text.
        
        '''
    )
    
    def __init__(self, huggingface_key):
        self.huggingface_api_token = huggingface_key
        pass
    
    def set_username(self, user_name : str) -> None:
        self.user_name = user_name
    
    def prompt_llm(self, prompt : str, prompt_template : PromptTemplate = None) -> str:
        llm = HuggingFaceHub(
        repo_id="ibm-granite/granite-3.0-3b-a800m-instruct",  # replace with the model name you want
        huggingfacehub_api_token=self.huggingface_api_token
        )
        if prompt_template:
            llm_chain = LLMChain(llm= llm, prompt= prompt_template)
            response = llm_chain.run(prompt)
        else:
            response = llm(prompt)

        return response

    def parse_model_output_to_dict(self, model_output):
        # Split the model output into lines and create a dictionary from it
        output_lines = model_output.strip().splitlines()
        result_dict = {}
        
        for line in output_lines:
            # Use regex to extract the field name and its numeric value
            match = re.match(r"(\w+):\s([\d.]+)", line)
            if match:
                key, value = match.groups()
                # Convert numeric values appropriately (int or float based on context)
                result_dict[key] = float(value) if '.' in value else int(value)
        
        return result_dict

    def parse_model_output_to_dataframe(self, model_output):
        # Use the dictionary function to parse the output first
        result_dict = self.parse_model_output_to_dict(model_output)
        
        # Convert dictionary to DataFrame with one row
        result_df = pd.DataFrame([result_dict])
        
        return result_df
    
    ########Pormpt functions##########
    #Returns text greeting the user according to its username. Must call set_username({user's_name}) first
    def greet_user(self) -> str:
        model_response = self.prompt_llm( prompt = self.user_name, prompt_template = self.greet_template)
        #Remove any additional text from the model's response.
        model_response = model_response.replace(f'''Greet a user called: {self.user_name} in a friendly but professional way.
                                                Please limit your response to a single line of text.
                                                In this context you are a web application that is going to recommend music to the user.
                                                Make the response a little bit different every time.''', '')
        return model_response
    
    #Returns a pandas DataFrame containing the additional values needed for a custon Spotify API Recommendations call.
    #The values are listed under the recommendation_template.
    def get_spotify_recommendation_data(self, user_input : str) -> pd.DataFrame:
        model_output = self.prompt_llm( prompt=user_input, prompt_template=self.spotify_data_template)
        return self.parse_model_output_to_dict(model_output=model_output)
    
    #Given a list of song names, this method returns a custom message for the user with his requested recommendations.
    def give_user_recommendations(self, songs_list : list[tuple], song_previews : list[str] = None) -> str:
        
        model_output = self.prompt_llm( prompt=self.user_name, prompt_template=self.custom_recommendation_template)
        response = model_output
        #Removes the instructions from the response
        response = model_output.replace(f'''The user's name is: {self.user_name}. Please let the user know, in a professional and friendly way, that you have a list of songs
        that you would like to recommend to them. In this context you are a web application that is going to recommend music to the user. Please limit your response to a single line of text.
        
        ''', '')
        response += '\n'
        i = 0
        for song_data in songs_list:
            response += '\n'        
            response += song_data[0] + ' by ' + song_data[1]
            if song_previews and song_previews[i] != None:
                response += ' preview url: ' + song_previews[i]
            i += 1   
        
        return response
    
    