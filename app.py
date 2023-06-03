from flask import Flask, request, render_template
import os
import requests, json

global translator_endpoint    
global cog_key    
global cog_region

try:
    cog_key = os.environ.get("COG_SERVICE_KEY")
    cog_region = os.environ.get("COG_SERVICE_REGION")  
    #cog_key = "a28f8e30d3d5461190103ed5d68226d9"
    #cog_region = "eastus"  
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'   
    #translator_endpoint='https://traductorbeatrizcognitive.cognitiveservices.azure.com/'
except Exception as ex:        
    print(ex)

app = Flask(__name__)

def GetLanguage(text):
    # # Default language is English
    language = 'en'
    # # Use the Translator detect function
    path = '/detect'
    url = translator_endpoint + path
    print(cog_key)
    # # Build the request
    params = {
         'api-version': '3.0'
     }

    headers = {
    'Ocp-Apim-Subscription-Key': cog_key,
    'Ocp-Apim-Subscription-Region': cog_region,
    'Content-type': 'application/json'
     }

    body = [{
         'text': text
     }]

    # # Send the request and get response
    request = requests.post(url, params=params, headers=headers, json=body)
    response = request.json()
    print(response)

    # # Parse JSON array and get language
    language = response[0]["language"]

    # # Return the language
    return language

def Translate(text, source_language):    
    translation = ''    
    # Use the Translator translate function    
    path = '/translate'    
    url = translator_endpoint + path    
    
    # Build the request    
    params = {        
              'api-version': '3.0',        
              'from': source_language,        
              'to': ['en']    
    }    
    
    headers = {        
               'Ocp-Apim-Subscription-Key': cog_key,        
               'Ocp-Apim-Subscription-Region': cog_region, 
               'Content-type': 'application/json'    
    }    
    body = [{        
             'text': text    
    }]    
    
    # Send the request and get response    
    request = requests.post(url, params=params, headers=headers, json=body)    
    response = request.json()    
    
    # Parse JSON array and get translation    
    translation = response[0]["translations"][0]["text"]    
    
    # Return the translation    
    return translation

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        print(text)
        
        # Aquí es donde procesarías el texto. Por ahora, solo devolvemos el mismo texto.
        source_language = GetLanguage(text)
        translated_text =  Translate(text, source_language)
        print(text)
        return render_template('home.html', translated_text=translated_text,lang_detected=source_language)
    
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
