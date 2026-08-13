import os
from google.genai import Client

def list_models():
    sa_path = os.path.join(os.path.dirname(__file__), "vertex_service_account.json")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = sa_path
    
    # Check Vertex AI models
    print("--- Listing models from Vertex AI ---")
    client_vertex = Client(vertexai=True, location='us-central1', project='light-depot-238403')
    try:
        models = client_vertex.models.list()
        for m in models:
            print(f"Model Name: {m.name}, Supported Actions: {m.supported_actions}")
    except Exception as e:
        print("Vertex AI listing error:", str(e))
        
    # Also check AI Studio models just in case (with the key, though it might fail due to 429, it might let us list)
    print("\n--- Listing models from AI Studio ---")
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    api_key = None
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.split("=")[1].strip()
                    break
    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    client_studio = Client(api_key=api_key)
    try:
        models = client_studio.models.list()
        for m in models:
            print(f"Model Name: {m.name}, Supported Actions: {m.supported_actions}")
    except Exception as e:
        print("AI Studio listing error:", str(e))

if __name__ == '__main__':
    list_models()
