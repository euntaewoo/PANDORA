import os
from google.genai import Client

def test_regions():
    sa_path = os.path.join(os.path.dirname(__file__), "vertex_service_account.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path
    
    regions = ['us-central1', 'us-east4', 'europe-west9', 'asia-northeast1']
    for r in regions:
        print(f"Testing region: {r} for gemini-3.1-pro-preview...")
        client = Client(vertexai=True, location=r, project='light-depot-238403')
        try:
            response = client.models.generate_content(
                model="gemini-3.1-pro-preview",
                contents="Hello! Test."
            )
            print(f"SUCCESS in {r}! Response: {response.text[:50]}")
            return r
        except Exception as e:
            print(f"FAILED in {r}: {str(e)[:150]}")

if __name__ == '__main__':
    test_regions()
