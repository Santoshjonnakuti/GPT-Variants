from flask import Flask, render_template, request
import openai

app = Flask(__name__)



@app.route("/", methods=["GET"])
def home():
  return render_template('index.html')

@app.route('/image-gpt', methods=['GET', 'POST'])
def imageGPT():
  if request.method == 'GET':
    return render_template('imagegpt.html')
  api_key = request.form['apiKey']
  openai.api_key = api_key
  prompt = request.form['input']
  error = ''
  url = ''
  if not len(prompt):
    error = 'Please Describe about the Image to Generate'
  elif not len(api_key):
    error = 'Please Provide OpenAI API Key'
  else:
    # Use OpenAI to generate an image
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    url = response['data'][0]['url']
  return render_template('imagegpt.html', url=url, inputValue=prompt, api_key=api_key, error=error)

@app.route("/audio-gpt", methods=["GET", "POST"])
def audioGPT():
  if request.method == 'GET':
    return render_template("audiogpt.html")
  error = ''
  transcription = ''
  api_key = request.form['apiKey']
  openai.api_key = api_key
  prompt = request.files['file']
  if not len(prompt.filename):
    error = 'Please Upload an audio to generate Transcript'
  elif not len(api_key):
    error = 'Please Provide OpenAI API Key'
  else:
    prompt.save(prompt.filename)
    # Use OpenAI to generate an image
    audio_file = open(prompt.filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    transcription = transcript['text']
  return render_template('audiogpt.html', text=transcription, inputValue=prompt.filename, api_key=api_key, error=error)
  
@app.route("/edits-gpt", methods=["GET", "POST"])
def editsGPT():
  if request.method == 'GET':
    return render_template("editsgpt.html")
  error = ''
  editedText = ''
  api_key = request.form['apiKey']
  openai.api_key = api_key
  text = request.form['text']
  prompt = request.form['prompt']
  if not len(text):
    error = 'Please Provide input text to Modify'
  elif not len(prompt):
    error = 'Please Provide Instruction to Modify the text'
  elif not len(api_key):
    error = 'Please Provide OpenAI API Key'
  else:
    response = openai.Edit.create(
      model="text-davinci-edit-001",
      input=text,
      instruction=prompt
    )
    editedText = response['choices'][0]['text']
  return render_template("editsgpt.html", text=editedText, inputValue=text, instruction=prompt, api_key=api_key,
                           error=error)

@app.route("/moderations-gpt", methods=["GET", "POST"])
def moderationsGPT():
  if request.method == 'GET':
    return render_template('moderationsgpt.html')
  error = ''
  moderations = ''
  api_key = request.form['apiKey']
  openai.api_key = api_key
  text = request.form['text']
  if not len(text):
    error = 'Please Provide input text to generate Moderations'
  elif not len(api_key):
    error = 'Please Provide OpenAI API Key'
  else:
    response = openai.Moderation.create(
      input=text,
    )
    moderations = response['results']
  return render_template('moderationsgpt.html', text=moderations, inputValue=text, api_key=api_key, error=error)
  
@app.route("/completions-gpt", methods=["GET", "POST"])
def completionsGPT():
  if request.method == 'GET':
    return render_template('completionsgpt.html')
  api_key = request.form['apiKey']
  openai.api_key = api_key
  text = request.form['text']
  error = ''
  completedText = ''
  if not len(text):
    error = 'Please Provide input text to Complete'
  elif not len(api_key):
    error = 'Please Provide OpenAI API Key'
  else:
    response = openai.Completion.create(
      model="text-davinci-003",
      prompt=text,
      max_tokens=800,
      temperature=0
    )
    completedText = text + ' ' + response['choices'][0]['text']
  return render_template('completionsgpt.html', text=completedText, inputValue=text, api_key=api_key, error=error)

@app.route("/audio-to-moderations-gpt", methods=["GET", "POST"])
def audioToModerations():
  if request.method == 'GET':
    return render_template('audioToModerationsgpt.html')
  api_key = request.form['apiKey']
  openai.api_key = api_key
  prompt = request.files['file']
  error = ''
  text = ''
  moderations = ''
  if not len(prompt.filename):
    error = 'Please Provide an audio file to generate Moderations'
  elif not len(api_key):
    error = 'Please Provide OpenAI API Key'
  else:
    prompt.save(prompt.filename)
    audio_file = open(prompt.filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text=transcript['text']
    response = openai.Moderation.create(
      input=text,
    )
    moderations =  response['results']
  return render_template('audioToModerationsgpt.html', text=text, table=moderations, inputValue=prompt, api_key=api_key, error=error)
    
@app.route("/audio-to-image-gpt", methods=["GET", "POST"])
def audioToImage():
  if request.method == 'GET':
    return render_template('audioToImagegpt.html')
  api_key = request.form['apiKey']
  openai.api_key = api_key
  prompt = request.files['file']
  text = ''
  url = ''
  error = ''
  if not len(prompt.filename):
    error = 'Please Provide an audio file to generate Image'
  elif not len(api_key):
    error = 'Please Provide OpenAI API Key'
  else:
    prompt.save(prompt.filename)
    audio_file = open(prompt.filename, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    text=transcript['text']
    response = openai.Image.create(
        prompt=text,
        n=1,
        size="1024x1024"
    )
    url = response['data'][0]['url']
  return render_template('audioToImagegpt.html', text=text, url=url, inputValue=prompt, api_key=api_key, error=error)

@app.route("/translate-gpt", methods=["GET", "POST"])
def tranlateGPT():
  if request.method == 'GET':
    return render_template('translationgpt.html')
  api_key = request.form['apiKey']
  openai.api_key = api_key
  prompt = request.files['file']
  text = ''
  error = ''
  if not len(prompt.filename):
    error = 'Please Provide an audio file to generate Image'
  elif not len(api_key):
    error = 'Please Provide OpenAI API Key'
  else:
    prompt.save(prompt.filename)
    audio_file = open(prompt.filename, "rb")
    transcript = openai.Audio.translate("whisper-1", audio_file)
    text = transcript['text']
  return render_template("translationgpt.html", text=text, inputValue=prompt, api_key=api_key, error=error)

if __name__ == '__main__':
  app.run(debug=False, port=8088, host='0.0.0.0')
