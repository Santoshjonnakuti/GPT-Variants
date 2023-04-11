from flask import Flask, render_template, request
import openai
import base64
from dotenv import load_dotenv
import os




# Load environment variables from .env file
load_dotenv()
# Set up OpenAI API credentials

api_key = os.environ.get('Ajay_KEY')

app = Flask(__name__)

openai.api_key = api_key


@app.route('/', methods=['GET', 'POST'])
def generate_image():
  if request.method == 'GET':
    return render_template('index.html', url=None, error=False)
  else:
    prompt = request.form['input']
    if not prompt:
      render_template('index.html', url='', error=True)
    # Use OpenAI to generate an image
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return render_template('index.html', url=response['data'][0]['url'], error=False)

@app.route("/audio-gpt", methods=["GET", "POST"])
def audioGPT():
  if request.method == 'GET':
    return render_template("audiogpt.html")
  else:
    prompt = request.files['file']
    print(prompt.filename)
    prompt.save(prompt.filename)
    if not prompt:
      render_template('audiogpt.html', url='', error=True)
    # Use OpenAI to generate an image
    audio_file = open(prompt.filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return render_template('audiogpt.html', text=transcript['text'])
  
if __name__ == '__main__':
    app.run(debug=True, port=8088)
