import os
from google.genai import Client

os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'D:\Users\euntaewoo\Desktop\JP_Ecom_Visual_Localizer_V3\vertex_service_account.json'
try:
    client = Client(vertexai=True, project='light-depot-238403', location='us-central1')
    models = client.models.list()
    for m in models:
        if 'gemini' in m.name.lower():
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
