import requests
import os

url = "https://api.play.ht/api/v2/cloned-voices"
headers = {
    "Authorization": f"Bearer {os.getenv("PLAY_HT_API_KEY")}",
    "X-User-ID": os.getenv("PLAY_HT_USER_ID"),
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("Request was successful!")
    print(response.json())
else:
    print("Failed to retrieve data:", response.status_code)
    print(response.text)
