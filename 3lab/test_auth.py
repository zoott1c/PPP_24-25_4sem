import requests

token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzQzODU5MDQxfQ.oe7IGWzDE-A8C5QksbbR7zL1ud6qWEKfBom4nN6cqRw"
headers = {
    "Authorization": token
}

response = requests.get("http://127.0.0.1:8000/users/me/", headers=headers)

print(response.status_code)
print(response.json())
