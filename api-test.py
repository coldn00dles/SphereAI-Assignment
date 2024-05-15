import json
import requests

url = "http://127.0.0.1:5050/api/chatbot/"
message = input("Enter your question related to the candidate : ")  # No need for str() as input() already returns a string
data = {"content" : message}

headers = {"Content-type": "application/json"}

# Making the request
response = requests.post(url, data=json.dumps(data), headers=headers)

# Checking for successful response
if response.ok:
    # Parsing JSON response
    try:
        json_response = response.json()
        output = json_response.get("output")
        if output is not None:
            print(output)
        else:
            print("No output found in response")
    except json.JSONDecodeError as e:
        print("Failed to decode JSON response:", e)
else:
    print("Request failed with status code:", response.status_code)
