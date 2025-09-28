from flask import Flask, request, jsonify
import os
import shutil
from gradio_client import Client, file
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app) 
# Initialize the Gradio client

# Resolve important paths relative to this file
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
FRONTEND_PUBLIC_DIR = os.path.join(PROJECT_ROOT, 'frontend', 'public')
UPLOADS_DIR = os.path.join(BACKEND_DIR, 'uploads')

os.makedirs(UPLOADS_DIR, exist_ok=True)
os.makedirs(FRONTEND_PUBLIC_DIR, exist_ok=True)

# External service URLs via environment variables (fallback to current defaults)
TRYON_URL = os.environ.get("TRYON_URL", "https://7395458a587bc50ec3.gradio.live/")
CHATBOT_URL = os.environ.get("CHATBOT_URL", "https://fe81ff40040ecfff3c.gradio.live/")
OCCASION_URL = os.environ.get("OCCASION_URL", "https://8c8e6f96c1fe2aefb7.gradio.live/")

def download_image(image_url):
    try:
        image_url = image_url.strip()
        if not image_url:
            raise ValueError("Image URL cannot be empty")

        # Name of the file to save the image as, with a .png extension
        filename = "downloaded_image.png"

        # Ensure the uploads directory exists
        if not os.path.exists(UPLOADS_DIR):
            os.makedirs(UPLOADS_DIR)

        # Full path to the file
        file_path = os.path.join(UPLOADS_DIR, filename)

        # Make the request to download the image with timeout
        response = requests.get(image_url, stream=True, timeout=30)

        # Check if the request was successful
        if response.status_code == 200:
            # Open the file in write mode and write the content
            with open(file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=128):
                    file.write(chunk)
            print(f"Image downloaded successfully and saved as {file_path}")
            return True
        else:
            print(f"Failed to download image. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading image: {str(e)}")
        return False


#try on
client = Client(TRYON_URL)

#chatBot
gradio_client = Client(CHATBOT_URL)

#dress
dress = Client("dhaan-ish/text-to-cloth")

#ocassion

ocassion_client = Client(OCCASION_URL)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field in request"}), 400
            
        text_input = data["text"]
        if not text_input or not text_input.strip():
            return jsonify({"error": "Text input cannot be empty"}), 400
            
        print(f"Processing text input: {text_input}")

        result = gradio_client.predict(
            text_input.strip(),	# str  in 'text' Textbox component
            api_name="/predict"
        )
        print(f"Prediction result: {result}")
        return jsonify({"result": result})
    except Exception as e:
        print(f"Error in predict: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/uploadocassion', methods=['POST'])
def upload_ocassion():
    try:
        # Check if the request contains a file
        print(request.files)
        if 'uploadedFile' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        uploaded_file = request.files['uploadedFile']
        if uploaded_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        # Check if URL is provided
        if 'url' not in request.form or not request.form['url'].strip():
            return jsonify({'error': 'URL is required'}), 400
            
        url = request.form['url'].strip()
        print(f"Processing URL: {url}")
        
        # Download image from URL
        download_image(url)
        
        if uploaded_file:
            # Save the uploaded file
            uploaded_file.save(os.path.join(UPLOADS_DIR, 'upload.png'))
            
            # Check if downloaded image exists
            downloaded_path = os.path.join(UPLOADS_DIR, "downloaded_image.png")
            if not os.path.exists(downloaded_path):
                return jsonify({'error': 'Failed to download image from URL'}), 400
            
            print("Processing virtual try-on...")
            # Use the Gradio client to make a prediction
            result = client.predict(
                file(downloaded_path), # filepath in 'cloth_image' Image component
                file(os.path.join(UPLOADS_DIR, "upload.png")), # filepath in 'origin_image' Image component
                api_name="/predict"
            )
            print(f"Try-on result: {result}")
            
            if not result or not os.path.exists(result):
                return jsonify({'error': 'Virtual try-on failed'}), 500
                
            destination_dir = FRONTEND_PUBLIC_DIR
            shutil.copy(result, destination_dir)
            
            return jsonify({'message': 'Result image copied successfully.'}), 200
    except Exception as e:
        print(f"Error in upload_ocassion: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/upload', methods=['POST'])
def upload_files():
    try:
        print(request.files)
        if 'uploadedFile' not in request.files:
            return jsonify({'error': 'No file part'}), 400
            
        uploaded_file = request.files['uploadedFile']
        if uploaded_file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
            
        if uploaded_file:
            # Save the uploaded file
            uploaded_file.save(os.path.join(UPLOADS_DIR, 'upload.png'))
            
            # Check if the default cloth image exists
            cloth_image_path = os.path.join(FRONTEND_PUBLIC_DIR, "image.JPEG")
            if not os.path.exists(cloth_image_path):
                return jsonify({'error': 'Default cloth image not found'}), 400
            
            print("Processing virtual try-on...")
            # Use the Gradio client to make a prediction
            result = client.predict(
                file(cloth_image_path), # filepath in 'cloth_image' Image component
                file(os.path.join(UPLOADS_DIR, "upload.png")), # filepath in 'origin_image' Image component
                api_name="/predict"
            )
            
            if not result or not os.path.exists(result):
                return jsonify({'error': 'Virtual try-on failed'}), 500
                
            print(f"Try-on result: {result}")
            destination_dir = FRONTEND_PUBLIC_DIR
            shutil.copy(result, destination_dir)
            
            return jsonify({'message': 'Result image copied successfully.'}), 200
    except Exception as e:
        print(f"Error in upload_files: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
@app.route('/handleprompt', methods=['POST'])
def handle_prompt():
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({'error': 'Missing prompt field'}), 400
            
        prompt = data.get('prompt')
        if not prompt or not prompt.strip():
            return jsonify({'error': 'Prompt cannot be empty'}), 400
            
        print(f"Processing prompt: {prompt}")
        result = dress.predict(
            prompt.strip(),
            api_name="/predict"
        )
        
        if not result or not os.path.exists(result):
            return jsonify({'error': 'Text-to-image generation failed'}), 500
            
        print(f"Generated image: {result}")
        dress_dir = FRONTEND_PUBLIC_DIR
        
        shutil.copy(result, dress_dir)
        print("Image generation completed successfully")
        return jsonify({'message': 'Success'}), 200
    except Exception as e:
        print(f"Error in handle_prompt: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/handleocassion', methods=['POST'])
def handleocassion():
    try:
        # Extract data from the request
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        color = data.get('color')
        selected_occasion = data.get('selectedOccasion')
        
        if not color or not color.strip():
            return jsonify({'error': 'Color is required'}), 400
        if not selected_occasion or not selected_occasion.strip():
            return jsonify({'error': 'Occasion is required'}), 400
            
        print(f"Processing: {color} shirt for {selected_occasion}")
        
        # Make the prediction
        result = ocassion_client.predict(
            f"{color.strip()} shirt for {selected_occasion.strip()}",
            api_name="/predict"
        )

        if not result:
            return jsonify({'error': 'Failed to get recommendations'}), 500

        # Process the result
        new_items = result.split(",") if isinstance(result, str) else []

        # Return the result as JSON
        return jsonify({
            'newItems': new_items,
            'showRecommendations': True
        })
    except Exception as e:
        print(f"Error in handleocassion: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
