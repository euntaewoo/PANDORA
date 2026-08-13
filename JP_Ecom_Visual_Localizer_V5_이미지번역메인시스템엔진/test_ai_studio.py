from google.genai import Client

def test_api():
    print("Testing AI Studio API Key...")
    client = Client(api_key="AIzaSyBbXAeLIYU72Diy5gwoJcG0A6Zd2uFVSUk")
    try:
        response = client.models.generate_content(
            model="gemini-3.1-pro-preview",
            contents="Hello, testing billing! Are you 3.1 Pro?"
        )
        print("SUCCESS! Response:", response.text)
    except Exception as e:
        print("ERROR:", str(e))

if __name__ == '__main__':
    test_api()
