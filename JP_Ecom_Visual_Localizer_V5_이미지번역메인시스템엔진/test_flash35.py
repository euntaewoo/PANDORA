import os
from google.genai import Client

def test_flash35():
    sa_path = os.path.join(os.path.dirname(__file__), "vertex_service_account.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path
    
    print("Testing gemini-3.5-flash on Vertex AI...")
    client = Client(vertexai=True, location='us-central1', project='light-depot-238403')
    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents="Hello! Are you 3.5 Flash?"
        )
        print("SUCCESS! Response:", response.text)
    except Exception as e:
        print("FAILED:", str(e))

if __name__ == '__main__':
    test_flash35()
