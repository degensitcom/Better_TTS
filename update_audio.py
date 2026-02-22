import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime, timedelta
from tts_api import *
from wav_downloader import *
from s3_uploader import *
# 1. Load the variables from .env into the environment
load_dotenv(dotenv_path="staging.env")
load_dotenv(dotenv_path="tts_creds.env")

# 2. Retrieve the URI
mongo_uri = os.getenv("MONGO_CONNECTION_STRING")
runpod_api_key = os.getenv("RUNPOD_API_KEY")
# 3. Connect safely
if not mongo_uri:
    print("Error: MONGO_CONNECTION_STRING not found in environment variables.")
else:
    client = MongoClient(mongo_uri)
    db = client["SCENARIO"] 
    collection = db["generated_scenario"]

    days_ago = datetime.now() - timedelta(days=1)
    query = {
    "new_tts_audio": {"$exists": False},
    "generation_time": {"$gte": days_ago}
    }
    results = collection.find(query)
    
    # Now you can run your filter
    
for scenario in results:
    total_cost = 0
    scenario_id = scenario.get('_id')
    dialogues = scenario.get("scenario", [])
    
    success = True
    for dialogue in dialogues:
        try:
            line = dialogue['line']
            character = dialogue['character']
            s3_path = dialogue['audio_path']

            # Generate Audio
            tts_response = generate_wav(line, character, runpod_api_key)
            download_url = tts_response["audio_url"]
            total_cost += tts_response.get("cost", 0)

            # Upload to S3
            stream_wav_to_s3(download_url, s3_path)
            
        except Exception as e:
            print(f"Failed processing line in {scenario_id}: {e}")
            success = False
            break # Stop this scenario if a line fails

    if success:
        # Mark as completed so it's not picked up next time
        collection.update_one(
            {"_id": scenario_id},
            {"$set": {"new_tts_audio": True, "total_tts_cost": total_cost}}
        )
        print(f"Finished scenario {scenario_id}. Total cost: {total_cost}")
            