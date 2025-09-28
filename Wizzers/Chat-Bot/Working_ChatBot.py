#!/usr/bin/env python3
"""
Working Fashion Chatbot with Gemini AI - No Dependency Conflicts!
This chatbot uses Google's Gemini API for intelligent fashion advice.
"""

import gradio as gr
import random
import os
import google.generativeai as genai
from pathlib import Path

# Initialize Gemini AI
def setup_gemini():
    """Setup Gemini AI with API key"""
    try:
        # Get API key from environment variable or use a default
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("⚠️  GEMINI_API_KEY not found in environment variables")
            print("   You can get your API key from: https://makersuite.google.com/app/apikey")
            print("   Set it with: export GEMINI_API_KEY='your_api_key_here'")
            return None
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        print("✅ Gemini AI initialized successfully!")
        return model
    except Exception as e:
        print(f"❌ Error initializing Gemini AI: {e}")
        return None

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
    "formal": [
        "Formal events require elegant attire: evening dresses, suits, or formal separates.",
        "Formal wear should be sophisticated: dark colors, quality fabrics, and appropriate accessories.",
        "Choose formal attire that fits well and makes you feel elegant and confident."
    ],
    "summer": [
        "Summer fashion: Light fabrics like cotton and linen, bright colors, and breathable materials.",
        "Summer colors: Pastels, whites, light blues, and bright floral patterns work well.",
        "Summer accessories: Sun hats, sunglasses, and light scarves for style and protection."
    ],
    "colors": [
        "Color coordination: Match complementary colors, use neutral tones as base, and add pops of color.",
        "Classic color combinations: Navy and white, black and white, or monochromatic schemes.",
        "Choose colors that complement your skin tone and make you feel confident."
    ],
    "accessories": [
        "Accessories: Simple jewelry, belts, scarves, and handbags can enhance any outfit.",
        "Less is more with accessories - choose pieces that complement rather than overwhelm your look.",
        "Quality accessories can elevate simple outfits and add personal style."
    ]
}

def get_fashion_advice(question, model=None):
    """Get fashion advice using Gemini AI or fallback to knowledge base"""
    
    if not question.strip():
        return "Please ask me a question about fashion! 💄"
    
    # Try Gemini AI first if available
    if model:
        try:
            prompt = f"""You are a professional fashion consultant and stylist. Provide helpful, detailed fashion advice for the following question. 
            
            Keep your response:
            - Practical and actionable
            - Professional yet friendly
            - Specific to the situation
            - Include styling tips and color suggestions
            - Keep it under 200 words
            
            Question: {question}
            
            Fashion Advice:"""
            
            response = model.generate_content(prompt)
            
            if response and response.text:
                return f"🤖 **AI Fashion Consultant:**\n\n{response.text}\n\n💡 *Powered by Google Gemini AI*"
            
        except Exception as e:
            print(f"⚠️  Gemini API error: {e}")
            print("   Falling back to knowledge base...")
    
    # Fallback to knowledge base
    question_lower = question.lower()
    advice = []
    
    if any(word in question_lower for word in ['interview', 'job', 'work', 'business', 'professional']):
        advice.extend(FASHION_KNOWLEDGE["interview"])
    elif any(word in question_lower for word in ['casual', 'relaxed', 'everyday', 'comfortable']):
        advice.extend(FASHION_KNOWLEDGE["casual"])
    elif any(word in question_lower for word in ['formal', 'elegant', 'dressy', 'special']):
        advice.extend(FASHION_KNOWLEDGE["formal"])
    elif any(word in question_lower for word in ['summer', 'hot', 'warm', 'season']):
        advice.extend(FASHION_KNOWLEDGE["summer"])
    elif any(word in question_lower for word in ['color', 'blue', 'red', 'black', 'white', 'green']):
        advice.extend(FASHION_KNOWLEDGE["colors"])
    elif any(word in question_lower for word in ['accessory', 'jewelry', 'belt', 'bag', 'scarf']):
        advice.extend(FASHION_KNOWLEDGE["accessories"])
    else:
        advice = [
            "Here are some general fashion tips: Always choose clothes that fit well and make you feel confident.",
            "Consider the occasion when selecting your outfit - dress appropriately for the setting.",
            "Quality over quantity - invest in a few well-made pieces rather than many cheap items.",
            "Don't forget about comfort - you should feel good in what you wear."
        ]
    
    response = random.choice(advice)
    response += "\n\n💡 Remember: The best outfit is one that makes you feel confident and comfortable!"
    
    return f"📚 **Fashion Knowledge Base:**\n\n{response}"

def create_interface(model=None):
    """Create the Gradio interface"""
    
    # Create a wrapper function that includes the model
    def chat_function(question):
        return get_fashion_advice(question, model)
    
    # Create the interface
    iface = gr.Interface(
        fn=chat_function,
        inputs=gr.Textbox(
            label="Ask about fashion",
            placeholder="What should I wear for a job interview?",
            lines=2
        ),
        outputs=gr.Textbox(
            label="Fashion Assistant Response",
            lines=10,
            show_copy_button=True
        ),
        title="🎭 AI Fashion Chatbot with Gemini",
        description="Ask me anything about fashion, styling, or clothing recommendations! Powered by Google Gemini AI.",
        theme=gr.themes.Soft(),
        examples=[
            ["What should I wear for a job interview?"],
            ["How to dress casually?"],
            ["What colors work best for summer?"],
            ["How to accessorize an outfit?"],
            ["What's appropriate for a business meeting?"],
            ["How to style a simple dress?"],
            ["What to wear for a formal event?"],
            ["How to coordinate colors?"],
            ["What shoes go with a navy suit?"],
            ["How to dress for a first date?"]
        ],
        cache_examples=True
    )
    
    return iface

def main():
    """Main function to run the chatbot"""
    
    print("🎭 AI Fashion Chatbot Starting...")
    print("=" * 60)
    
    # Setup Gemini AI
    model = setup_gemini()
    
    if model:
        print("✅ Gemini AI ready!")
        print("🤖 AI-powered fashion advice available!")
    else:
        print("📚 Using knowledge base fallback")
        print("💡 Get Gemini API key for AI-powered responses!")
    
    print("=" * 60)
    
    # Create and launch interface
    iface = create_interface(model)
    
    print("🚀 Launching AI Fashion Chatbot...")
    print("The interface will open in your browser shortly...")
    
    try:
        iface.launch(
            debug=True,
            share=True,  # Creates a public link
            server_name="0.0.0.0",
            server_port=7860
        )
    except Exception as e:
        print(f"❌ Error launching: {e}")
        print("Trying without sharing...")
        try:
            iface.launch(debug=True, share=False)
        except Exception as e2:
            print(f"❌ Failed to launch: {e2}")
            print("Please check if port 7860 is available.")

if __name__ == "__main__":
    main()
