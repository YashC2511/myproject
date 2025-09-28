# 🎭 Fashion Chatbot

A smart fashion assistant powered by RAG (Retrieval Augmented Generation) using LlamaIndex and Mistral-7B.

## 🚀 Quick Start

### Option 1: Automatic Setup (Recommended)

1. **Run the setup script:**
   ```bash
   python setup_and_run.py
   ```

2. **Add your fashion document:**
   - Place your `fashion.pdf` file in the `Data` folder
   - The script will guide you through this

3. **Wait for setup to complete:**
   - Models will be downloaded (4.3GB for Mistral-7B)
   - This may take 5-10 minutes depending on your internet speed

4. **Access your chatbot:**
   - A Gradio interface will open in your browser
   - You'll get a public link to share with others

### Option 2: Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Jupyter notebook:**
   ```bash
   jupyter notebook ChatBot.ipynb
   ```

3. **Execute cells in order:**
   - Run all cells from top to bottom
   - Wait for models to load

## 📁 File Structure

```
Chat-Bot/
├── ChatBot.ipynb          # Main Jupyter notebook
├── setup_and_run.py       # Quick setup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
└── Data/
    └── fashion.pdf       # Your fashion document (add this)
```

## 🔧 Requirements

- **Python 3.8+**
- **8GB+ RAM** (recommended for Mistral-7B)
- **Internet connection** (for model download)
- **Fashion document** (PDF format)

## 💡 Usage Examples

Ask questions like:
- "What should I wear for a job interview?"
- "How to style a casual outfit?"
- "What colors work best for summer?"
- "How to accessorize a simple dress?"

## 🛠️ Troubleshooting

### Common Issues:

1. **"fashion.pdf not found"**
   - Add your fashion document to the `Data` folder
   - Ensure it's named `fashion.pdf`

2. **"Model loading failed"**
   - Check your internet connection
   - Ensure you have enough RAM (8GB+)
   - Try running again after a few minutes

3. **"Port 7860 already in use"**
   - Close other applications using port 7860
   - Or change the port in the launch configuration

4. **"CUDA out of memory"**
   - The system will automatically fallback to CPU
   - This will be slower but will work

### Getting Help:

- Check the console output for detailed error messages
- Ensure all dependencies are installed correctly
- Try running the setup script again

## 🎯 Features

- **Smart Document Analysis**: Understands your fashion documents
- **Contextual Responses**: Provides relevant fashion advice
- **Beautiful Interface**: Professional Gradio web interface
- **Example Questions**: Pre-loaded fashion questions to get started
- **Error Handling**: Robust error handling with helpful messages

## 📝 Notes

- First run will take longer due to model downloads
- The system uses local models for privacy
- Responses are based on your uploaded documents
- Interface supports conversation history and examples

## 🔗 Links

- **Gradio Interface**: Opens automatically after setup
- **Public Link**: Share with others (72-hour expiry for free accounts)
- **Local Access**: http://localhost:7860

Enjoy your fashion chatbot! 🎉
