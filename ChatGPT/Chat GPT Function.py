# You may need to install the openai library and can do so with the code below.
# pip install openai
# conda install -c conda-forge openai

#The 

import openai
import os

#Generate an Open AI API key by signing up and creating a new secret key
#For easier use, you can set an environment variable APIKEY and store it that way
#openai.api_key= os.environ.get('APIKEY')
openai.api_key  = ''


def Chat_GPT_Helper_Function(prompt, model="gpt-3.5-turbo-16k"):
    # This assignes the role and the content to be passed to the OpenAI API. 
    messages = [{"role": "user", "content": prompt}]

    # This is the function to actually get a response from the API. 
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        max_tokens=100, # The max number of tokens to generate.
        #echo=False, # Whether to return the prompt in addition to the generated completion
        temperature=0, # What sampling temperature to use, between 0 and 2, higher values will make the output more random. 
        #top_p=1.0, # An alternative to sampling with temperature, where the model considers the results of the tokens with top_p probability. 
        #frequency_penalty=0.0, # Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text.
        #presence_penalty=0.0, # Number between -2.0 and 2.0. Positive values penalize new tokens based on whether they appear in the text so far, increasing the model's likelihood to talk about new topics.
        stop=["/4/"] # Up to 4 sequences where the API will stop generating further tokens.
    )
    return response.choices[0].message["content"]

text = f"""
Black Schole's model
"""
# This is where you define the prompt to send to the model.
prompt = f"""
Give me the equation for the below and explain how to calculate each variable
```{text}```
"""
response = Chat_GPT_Helper_Function(prompt)
print(response)

