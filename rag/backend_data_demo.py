import requests

# Backend API endpoint
url = "http://127.0.0.1:8000/api/events"

# Get event data from backend
response = requests.get(url)

print("Status code:", response.status_code)

if response.status_code == 200:
    events = response.json()

    print("\nEvents received from backend:")
    print(events)
else:
    print("\nCould not connect to the backend.")
    print(response.text)