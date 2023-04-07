from flask import Flask, render_template
import openai
import base64

app = Flask(__name__)

# Set up OpenAI API credentials
openai.api_key = 'YOUR_API_KEY_HERE'

@app.route('/')
def generate_image():
    # Use OpenAI to generate an image
    response = openai.Image.create(
        prompt="Generate an image of a cat",
        n=1,
        size="1024x1024"
    )

    # Convert the image data to base64 encoding
    image_data = base64.b64encode(response['data']).decode()

    # Render the image on a webpage
    return render_template('image.html', image_data=image_data)
