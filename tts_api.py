import requests

# Define the API endpoint and your credentials
# url = "https://api.runpod.ai/v2/chatterbox-turbo/run"
ENDPOINT_ID = "chatterbox-turbo"
call_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/run"
import time
def generate_wav(line,character,api_key):

    # The dynamic URL using an f-string
    voice_url = f"https://raw.githubusercontent.com/degensitcom/Better_TTS/main/Audio_samples/{character}/{character.lower()}.wav"
    
    # Define the payload
    data = {
        "input": {
            "prompt": line,
            "voice": "dylan",
            "format": "wav",
            "voice_url": voice_url
        }
    }

    # Set up the headers
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    # 1. Kick off the job
    # Make the POST request
    response = requests.post(call_url, json=data, headers=headers)
    print(response)
    job_id = response.json().get("id")
    print(f"Job started. ID: {job_id}")

    # 2. Poll for the output
    status_url = f"https://api.runpod.ai/v2/{ENDPOINT_ID}/status/{job_id}"
    while True:
            status_res = requests.get(status_url, headers=headers).json()
            status = status_res.get("status")

            if status == "COMPLETED":
                print("Job Finished!")
                return status_res.get("output") # This is usually your URL or data
            
            elif status == "FAILED":
                print("Job Failed.")
                return None
            else:
                print(f"Status: {status}... waiting 2 seconds.")
                time.sleep(2)
