import os
import io
import requests
import boto3
from dotenv import load_dotenv


def stream_wav_to_s3(download_url, s3_path):

    # 1. Setup S3 Client
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION")
    )
    bucket = os.getenv("S3_BUCKET_NAME")
    
    try:
        # 2. Get the file from RunPod into memory
        print(f"Downloading from RunPod...")
        response = requests.get(download_url)
        response.raise_for_status()
        
        # Wrap the content in a BytesIO object (virtual file)
        audio_stream = io.BytesIO(response.content)
        
        # 3. Upload directly to S3
        print(f"Streaming directly to S3: {s3_path}")
        s3.upload_fileobj(
            audio_stream, 
            bucket, 
            s3_path,
            ExtraArgs={'ContentType': 'audio/wav'} # Ensures it plays in browsers
        )
        print("Done!")
        return True

    except Exception as e:
        print(f"Error in stream: {e}")
        return False
