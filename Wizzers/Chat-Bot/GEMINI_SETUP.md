# 🤖 Gemini API Setup Guide

## How to Get Your Gemini API Key

### Step 1: Get API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key

### Step 2: Set Environment Variable

#### Option A: In Colab
```python
import os
os.environ['GEMINI_API_KEY'] = 'your_api_key_here'
```

#### Option B: In Terminal (Linux/Mac)
```bash
export GEMINI_API_KEY='your_api_key_here'
```

#### Option C: In Command Prompt (Windows)
```cmd
set GEMINI_API_KEY=your_api_key_here
```

#### Option D: Create .env file
Create a `.env` file in your project directory:
```
GEMINI_API_KEY=your_api_key_here
```

### Step 3: Install Dependencies
```bash
pip install -r simple_requirements.txt
```

### Step 4: Run the Chatbot
```bash
python Working_ChatBot.py
```

## Features with Gemini AI

✅ **Intelligent Responses**: Context-aware fashion advice
✅ **Detailed Styling Tips**: Specific recommendations for different occasions
✅ **Color Coordination**: Smart color matching suggestions
✅ **Seasonal Advice**: Weather-appropriate clothing recommendations
✅ **Personalized Suggestions**: Tailored advice based on your questions

## Fallback System

If Gemini API is not available, the chatbot automatically falls back to the built-in knowledge base, so it will always work!

## Example Questions

- "What should I wear for a job interview at a tech startup?"
- "How to dress for a summer wedding as a guest?"
- "What colors work best with my skin tone?"
- "How to style a blazer for casual Friday?"
- "What accessories go with a little black dress?"
