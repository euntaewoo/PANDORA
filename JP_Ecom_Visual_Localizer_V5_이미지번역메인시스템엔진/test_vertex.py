import os
from google.genai import Client

def test_vertex():
    print("Testing Vertex AI 2.5 Pro...")
    sa_path = os.path.join(os.path.dirname(__file__), "vertex_service_account.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path
    client = Client(vertexai=True, location='us-central1', project='light-depot-238403')
    try:
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents="Hello Vertex! Are you 2.5 Pro?"
        )
        print("SUCCESS! Response:", response.text)
    except Exception as e:
        print("ERROR:", str(e))

if __name__ == '__main__':
    test_vertex()
