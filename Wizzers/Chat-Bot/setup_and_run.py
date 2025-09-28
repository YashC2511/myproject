#!/usr/bin/env python3
"""
Quick setup and run script for the Fashion Chatbot
Run this script to automatically set up and launch the chatbot
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    
    packages = [
        "gradio",
        "pypdf", 
        "python-dotenv",
        "transformers",
        "langchain",
        "llama-index",
        "llama-index-embeddings-huggingface",
        "llama-index-llms-llama-cpp",
        "llama-index-embeddings-langchain",
        "sentence-transformers",
        "torch"
    ]
    
    for package in packages:
        try:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package, '-q'])
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Warning: Failed to install {package}: {e}")
    
    print("✅ Package installation completed!")

def setup_data_directory():
    """Set up data directory"""
    print("📁 Setting up data directory...")
    
    data_dir = Path("Data")
    data_dir.mkdir(exist_ok=True)
    
    fashion_pdf = data_dir / "fashion.pdf"
    if not fashion_pdf.exists():
        print("⚠️  fashion.pdf not found in Data folder!")
        print("   Please add your fashion document to the Data folder.")
        print("   You can download a sample fashion document or add your own.")
        return False
    else:
        print(f"✅ Found fashion document: {fashion_pdf}")
        return True

def run_chatbot():
    """Run the chatbot"""
    print("🚀 Starting Fashion Chatbot...")
    
    try:
        # Import and run the chatbot code
        exec(open('chatbot_main.py').read())
    except FileNotFoundError:
        print("❌ chatbot_main.py not found. Creating it now...")
        create_main_script()
        exec(open('chatbot_main.py').read())

def create_main_script():
    """Create the main chatbot script"""
    print("📝 Creating main chatbot script...")
    
    script_content = '''
import logging
import sys
import os
from pathlib import Path

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Import LlamaIndex components
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.llama_cpp.llama_utils import messages_to_prompt, completion_to_prompt
from llama_index.embeddings.langchain import LangchainEmbedding
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import gradio as gr

print("✅ Using modern LlamaIndex API (no deprecated ServiceContext)")

def setup_models():
    """Set up the embedding model and LLM"""
    print("🔤 Setting up embedding model...")
    
    try:
        embed_model = LangchainEmbedding(
            HuggingFaceEmbeddings(model_name="thenlper/gte-large")
        )
        print("✅ Embedding model loaded!")
    except Exception as e:
        print(f"⚠️  Using fallback embedding model: {e}")
        from llama_index.embeddings.huggingface import HuggingFaceEmbedding
        embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    print("🤖 Setting up Mistral-7B model...")
    
    try:
        llm = LlamaCPP(
            model_url='https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf',
            model_path=None,
            temperature=0.1,
            max_new_tokens=256,
            context_window=3900,
            generate_kwargs={},
            model_kwargs={"n_gpu_layers": -1},
            messages_to_prompt=messages_to_prompt,
            completion_to_prompt=completion_to_prompt,
            verbose=True,
        )
        print("✅ Mistral-7B model loaded!")
    except Exception as e:
        print(f"❌ Error loading Mistral-7B: {e}")
        print("⚠️  This might take several minutes to download (4.3GB)")
        return None, None
    
    # Configure settings
    Settings.llm = llm
    Settings.embed_model = embed_model
    Settings.chunk_size = 256
    Settings.chunk_overlap = 20
    
    return llm, embed_model

def create_index():
    """Create the vector store index"""
    print("📚 Creating vector store index...")
    
    try:
        data_dir = Path("Data")
        documents = SimpleDirectoryReader(str(data_dir)).load_data()
        print(f"✅ Loaded {len(documents)} document(s)")
        
        index = VectorStoreIndex.from_documents(documents)
        query_engine = index.as_query_engine()
        print("✅ Index created successfully!")
        
        return query_engine
    except Exception as e:
        print(f"❌ Error creating index: {e}")
        return None

def fashion_chatbot(question):
    """Chatbot function"""
    try:
        if not question.strip():
            return "Please ask a question about fashion!"
        
        response = query_engine.query(question)
        return str(response)
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

def main():
    """Main function"""
    print("🎭 Fashion Chatbot Setup")
    print("=" * 50)
    
    # Setup models
    llm, embed_model = setup_models()
    if llm is None:
        print("❌ Failed to load models. Please check your setup.")
        return
    
    # Create index
    global query_engine
    query_engine = create_index()
    if query_engine is None:
        print("❌ Failed to create index. Please check your documents.")
        return
    
    # Create interface
    print("🎨 Creating Gradio interface...")
    
    iface = gr.Interface(
        fn=fashion_chatbot,
        inputs=gr.Textbox(
            label="Ask about fashion",
            placeholder="What should I wear for a job interview?",
            lines=2
        ),
        outputs=gr.Textbox(
            label="Fashion Assistant Response",
            lines=8,
            show_copy_button=True
        ),
        title="🎭 Fashion Chatbot Assistant",
        description="Ask me anything about fashion, styling, or clothing recommendations!",
        theme=gr.themes.Soft(),
        examples=[
            ["What should I wear for a job interview?"],
            ["How to style a casual outfit?"],
            ["What colors work best for summer?"],
            ["How to accessorize a simple dress?"]
        ]
    )
    
    print("🚀 Launching Fashion Chatbot...")
    print("The interface will open in your browser shortly...")
    
    try:
        iface.launch(
            debug=True,
            share=True,
            server_name="0.0.0.0",
            server_port=7860
        )
    except Exception as e:
        print(f"❌ Error launching: {e}")
        print("Trying without sharing...")
        iface.launch(debug=True, share=False)

if __name__ == "__main__":
    main()
'''
    
    with open('chatbot_main.py', 'w') as f:
        f.write(script_content)
    
    print("✅ Main script created!")

def main():
    """Main setup function"""
    print("🎭 Fashion Chatbot Quick Setup")
    print("=" * 50)
    
    # Install requirements
    install_requirements()
    
    # Setup data directory
    if not setup_data_directory():
        print("\n📝 Please add your fashion document to the Data folder and run again.")
        return
    
    # Run chatbot
    run_chatbot()

if __name__ == "__main__":
    main()
