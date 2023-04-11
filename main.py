from flask import Flask, render_template, request, redirect
import openai
import base64
from dotenv import load_dotenv
import os
import speech_recognition as sr



# Load environment variables from .env file
load_dotenv()
# Set up OpenAI API credentials

api_key = os.environ.get('OPENAI_KEY')

app = Flask(__name__)

openai.api_key = api_key


@app.route("/", methods=["GET"])
def home():
  return render_template('index.html')
@app.route('/image-gpt', methods=['GET', 'POST'])
def generate_image():
  if request.method == 'GET':
    return render_template('imagegpt.html', url=None, error=False)
  else:
    prompt = request.form['input']
    if not prompt:
      render_template('imagegpt.html', url='', error=True)
    # Use OpenAI to generate an image
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return render_template('imagegpt.html', url=response['data'][0]['url'], error=False)

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
  
@app.route("/edits-gpt", methods=["GET", "POST"])
def editsGPT():
  if request.method == 'GET':
    return render_template("editsgpt.html")
  else:
    text = request.form['text']
    prompt = request.form['prompt']
    print(text, prompt)
    response = openai.Edit.create(
      model="text-davinci-edit-001",
      input=text,
      instruction=prompt
    )
    print(response)
    return render_template("editsgpt.html", text=response['choices'][0]['text'])

@app.route("/moderations-gpt", methods=["GET", "POST"])
def moderationsGPT():
  if request.method == 'GET':
    return render_template('moderationsgpt.html')
  else:
    text = request.form['text']
    response = openai.Moderation.create(
      input=text,
    )
    print(response)
    return render_template('moderationsgpt.html', text=response['results'])
  
@app.route("/completions-gpt", methods=["GET", "POST"])
def completionsGPT():
  if request.method == 'GET':
    return render_template('completionsgpt.html')
  else:
    text = request.form['text']
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=text,
      max_tokens=800,
      temperature=0
    )
    print(response)
    return render_template('completionsgpt.html', text=text + ' ' + response['choices'][0]['text'])

@app.route("/audio-to-moderations-gpt", methods=["GET", "POST"])
def audioToModerations():
  if request.method == 'GET':
    return render_template('audioToModerationsgpt.html')
  else:
    prompt = request.files['file']
    print(prompt.filename)
    prompt.save(prompt.filename)
    audio_file = open(prompt.filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text=transcript['text']
    response = openai.Moderation.create(
      input=text,
    )
    print(response)
    return render_template('audioToModerationsgpt.html', text=text, table=response['results'])
    
@app.route("/audio-to-image-gpt", methods=["GET", "POST"])
def audioToImage():
  if request.method == 'GET':
    return render_template('audioToImagegpt.html')
  else:
    prompt = request.files['file']
    print(prompt.filename)
    prompt.save(prompt.filename)
    audio_file = open(prompt.filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text=transcript['text']
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="1024x1024"
    )
    return render_template('audioToImagegpt.html', text=text, url=response['data'][0]['url'])

@app.route("/translate-gpt", methods=["GET", "POST"])
def tranlateGPT():
  if request.method == 'GET':
    return render_template('translationgpt.html')
  prompt = request.files['file']
  print(prompt.filename)
  prompt.save(prompt.filename)
  audio_file = open(prompt.filename, "rb")
  transcript = openai.Audio.translate("whisper-1", audio_file)
  return render_template("translationgpt.html", text=transcript['text'])

if __name__ == '__main__':
    app.run(debug=True, port=8088)
