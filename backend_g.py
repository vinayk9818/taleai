from flask import Flask ,render_template,request
from gtts import gTTS
import requests
from dotenv import load_dotenv
import os

app=Flask(__name__)

load_dotenv()
@app.route("/",methods=['POST','GET'])
def teller():
    story=""
    if request.method=='POST':
        user_input=request.form.get('user_input')

        headers={
            "Authorization":os.getenv("secret_key"),
            "Content-type":os.getenv("mode")
        }
        
        data={
            "model":"llama3-70b-8192",
            "messages":[
                {"role":"system","content":"you are a funny joke teller"},
                {"role":"user","content":user_input}
            ]
        }

        response=requests.post("https://api.groq.com/openai/v1/chat/completions",headers=headers,json=data)
        story=response.json()['choices'][0]['message']['content']

        tts=gTTS(text=story,lang='hi')
        tts.save("static/story.mp3")
    return render_template('page.html',story=story)

if __name__=="__main__":
    app.run(debug=True)