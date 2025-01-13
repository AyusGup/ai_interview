import requests

url = "http://127.0.0.1:5000/analyze-image"  # URL for the FastAPI endpoint
file_path = "passport-photo.jpg"  # Replace with the path to your image file

# Data to be sent along with the image
data = {
    "user_id": "6772a7839f17be85486b1f82",  # Replace with actual user_id
    "interview_id": "6772a648652fdff0a3c339ba",  # Replace with actual interview_id
    "question_id": "6772a574a19e5eedb1d94ebe",  # Replace with actual question_id
}

# Open the image file in binary mode
with open(file_path, "rb") as file:
    # Prepare the files dictionary, which will include the file to upload
    files = {"file": (file_path, file, "image/jpg")}  # Adjust content type if needed

    # Send the POST request to the FastAPI server with both the file and the data
    response = requests.post(url, files=files, data=data)

# Check the response from the server
print(f"Status Code: {response.status_code}")
print("Response JSON:", response.json())
