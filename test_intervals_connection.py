import requests
import base64
import json

# API credentials
api_key = "7ghfnbbbo6s"

# API endpoint
base_url = "https://api.myintervals.com"
endpoint = "/me"
url = f"{base_url}{endpoint}"

# Try different authentication methods
print("Testing different authentication methods...")

# Method 1: API key as username, empty password
print("\nMethod 1: API key as username, empty password")
auth1 = (api_key, "")
response1 = requests.get(url, auth=auth1)
print(f"Status Code: {response1.status_code}")
print(f"Response: {response1.text}")

# Method 2: Empty username, API key as password
print("\nMethod 2: Empty username, API key as password")
auth2 = ("", api_key)
response2 = requests.get(url, auth=auth2)
print(f"Status Code: {response2.status_code}")
print(f"Response: {response2.text}")

# Method 3: API key as both username and password
print("\nMethod 3: API key as both username and password")
auth3 = (api_key, api_key)
response3 = requests.get(url, auth=auth3)
print(f"Status Code: {response3.status_code}")
print(f"Response: {response3.text}")

# Method 4: Using token in URL
print("\nMethod 4: Using token in URL")
url_with_token = f"{url}?token={api_key}"
response4 = requests.get(url_with_token)
print(f"Status Code: {response4.status_code}")
print(f"Response: {response4.text}")

# Method 5: Using Authorization header with Bearer token
print("\nMethod 5: Using Authorization header with Bearer token")
headers5 = {"Authorization": f"Bearer {api_key}"}
response5 = requests.get(url, headers=headers5)
print(f"Status Code: {response5.status_code}")
print(f"Response: {response5.text}") 