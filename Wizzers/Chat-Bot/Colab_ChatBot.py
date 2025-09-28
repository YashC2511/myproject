# 🎭 AI Fashion Chatbot for Google Colab
# Run this entire cell to get your fashion chatbot working immediately!

# Install required packages
!pip install -q gradio google-generativeai

# Import libraries
import gradio as gr
import os
import google.generativeai as genai
import random

# Fashion knowledge base (fallback)
FASHION_KNOWLEDGE = {
    "interview": [
        "For job interviews, wear professional attire: dark suits (navy or black), white or light blue shirts, closed-toe shoes.",
        "Professional dress code: Conservative colors, well-fitted clothes, minimal jewelry, and polished shoes.",
        "Interview attire should be clean, pressed, and make you feel confident and professional."
    ],
    "casual": [
        "Casual wear: Jeans with nice blouses or polo shirts, comfortable sneakers or flats.",
        "Casual outfits work well with denim, cotton shirts, and comfortable shoes for everyday activities.",
        "Keep casual wear clean, comfortable, and appropriate for the occasion."
    ],
    "summer": [
        "Summer fashion: Light fabrics like cotton and linen, bright colors, and breathable materials.",
        "Summer colors: Pastels, whites, light blues, and bright floral patterns work well.",
        "Summer accessories: Sun hats, sunglasses, and light scarves for style and protection."
    ]
}

def setup_gemini():
    """Setup Gemini AI with API key"""
    try:
        # Check if API key is set
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️  GEMINI_API_KEY not found!")
            print("   Set it with: os.environ['GEMINI_API_KEY'] = 'your_api_key_here'")
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini AI initialized!")
        return model
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_fashion_advice(question, model=None):
    """Get fashion advice using Gemini AI or fallback"""
    
    if not question.strip():
        return "Please ask me a question about fashion! 💄"
    
    # Try Gemini AI first
    if model:
        try:
            prompt = f"""You are a professional fashion consultant. Provide helpful fashion advice for: {question}
            
            Keep response:
            - Practical and actionable
            - Professional yet friendly  
            - Under 200 words
            - Include styling tips
            
            Fashion Advice:"""
            
            response = model.generate_content(prompt)
            if response and response.text:
                return f"🤖 **AI Fashion Consultant:**\n\n{response.text}\n\n💡 *Powered by Google Gemini AI*"
                
        except Exception as e:
            print(f"⚠️  Gemini error: {e}")
    
    # Fallback to knowledge base
    question_lower = question.lower()
    advice = []
    
    if any(word in question_lower for word in ['interview', 'job', 'work', 'business']):
        advice.extend(FASHION_KNOWLEDGE["interview"])
    elif any(word in question_lower for word in ['casual', 'relaxed', 'everyday']):
        advice.extend(FASHION_KNOWLEDGE["casual"])
    elif any(word in question_lower for word in ['summer', 'hot', 'warm']):
        advice.extend(FASHION_KNOWLEDGE["summer"])
    else:
        advice = ["Choose clothes that fit well and make you feel confident. Consider the occasion and dress appropriately."]
    
    response = random.choice(advice)
    return f"📚 **Fashion Knowledge:**\n\n{response}\n\n💡 Remember: Confidence is the best accessory!"

# Setup Gemini
model = setup_gemini()

# Create Gradio interface
iface = gr.Interface(
    fn=lambda question: get_fashion_advice(question, model),
    inputs=gr.Textbox(label="Ask about fashion", placeholder="What should I wear for a job interview?", lines=2),
    outputs=gr.Textbox(label="Fashion Advice", lines=8, show_copy_button=True),
    title="🎭 AI Fashion Chatbot",
    description="Ask me anything about fashion! Powered by Google Gemini AI.",
    examples=[
        ["What should I wear for a job interview?"],
        ["How to dress casually?"],
        ["What colors work for summer?"],
        ["How to accessorize an outfit?"]
    ]
)

print("🚀 Launching Fashion Chatbot...")
iface.launch(share=True, debug=True)

