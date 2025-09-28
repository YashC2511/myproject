# Wizzers Backend

A Flask-based backend for the Wizzers fashion application with virtual try-on, chatbot, and outfit recommendation features.

## Features

- **Virtual Try-On**: Upload images and try on different clothing items
- **Chatbot**: AI-powered fashion assistant
- **Text-to-Image**: Generate clothing images from text prompts
- **Occasion-based Recommendations**: Get outfit suggestions for specific occasions

## Setup Instructions

### 1. Install Dependencies

Run the automatic installation script:
```bash
python install_dependencies.py
```

Or install manually:
```bash
pip install -r requirements.txt
```

### 2. Required Dependencies

- Flask 2.3.3
- Flask-CORS 4.0.0
- gradio-client 0.7.0
- requests 2.31.0

### 3. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000` with debug mode enabled.

### 4. Test the Setup

Run the test script to verify Gradio connections:
```bash
python test.py
```

## API Endpoints

### POST /predict
Chatbot endpoint for text-based interactions.

**Request Body:**
```json
{
  "text": "What should I wear for a job interview?"
}
```

### POST /upload
Virtual try-on with default cloth image.

**Request:** Multipart form with `uploadedFile`

### POST /uploadocassion
Virtual try-on with custom cloth image from URL.

**Request:** 
- Multipart form with `uploadedFile` (person image)
- Form field `url` (cloth image URL)

### POST /handleprompt
Generate clothing images from text prompts.

**Request Body:**
```json
{
  "prompt": "A red dress for a summer party"
}
```

### POST /handleocassion
Get outfit recommendations for specific occasions.

**Request Body:**
```json
{
  "color": "blue",
  "selectedOccasion": "business meeting"
}
```

## Environment Variables

You can configure external service URLs using environment variables:

- `TRYON_URL`: Virtual try-on service URL
- `CHATBOT_URL`: Chatbot service URL  
- `OCCASION_URL`: Occasion recommendation service URL

## Directory Structure

```
backend/
├── app.py                 # Main Flask application
├── test.py               # Test script for Gradio connections
├── requirements.txt      # Python dependencies
├── install_dependencies.py # Setup script
├── uploads/              # Temporary file storage
└── README.md            # This file
```

## Error Handling

The application includes comprehensive error handling for:
- Missing or invalid request data
- File upload issues
- External service failures
- Network timeouts
- File system errors

## Troubleshooting

### Import Errors
If you see import errors, make sure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### External Service Issues
Check that the Gradio service URLs are accessible and the services are running.

### File Upload Issues
Ensure the `uploads/` directory exists and has write permissions.

### CORS Issues
The application includes Flask-CORS for cross-origin requests. Make sure your frontend is properly configured.
