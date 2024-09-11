import time
import random
import requests

def api_call_with_exponential_backoff(url, max_retries = 3):
    retry_delay = 1
    for attempt in range(max_retries):
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            time.sleep(retry_delay)
            retry_delay *= 2
            retry_delay += random.uniform(0, 1)
            
    raise Exception(f'Maximum retry attempts reached!')