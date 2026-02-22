import requests

def download_wav(url, destination):
    try:
        # Send a GET request
        with requests.get(url, stream=True) as r:
            r.raise_for_status() # Check for errors (404, 500, etc)
            
            # Write the file in chunks
            with open(destination, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
                    
        print(f"Download complete: {destination}")
        return True
    except Exception as e:
        print(f"Failed to download: {e}")
        return False

