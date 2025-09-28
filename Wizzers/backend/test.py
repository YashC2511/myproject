from gradio_client import Client, file

def test_gradio_connection():
    """Test the Gradio client connection and prediction."""
    try:
        print("Testing Gradio client connection...")
        client = Client("https://7395458a587bc50ec3.gradio.live/")
        
        print("Making prediction...")
        result = client.predict(
            file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),	# filepath in 'cloth_image' Image component
            file('https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png'),	# filepath in 'origin_image' Image component
            api_name="/predict"
        )
        print(f"✅ Prediction successful! Result: {result}")
        return True
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_gradio_connection()