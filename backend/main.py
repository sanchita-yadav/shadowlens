import requests
from flask import Flask, jsonify, request
app = Flask(__name__)
@app.route("/")
def home():
    return "ShadowLens backend is running!"
@app.route("/analyze")
def analyze():
    username = request.args.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "GitHub username not found"}), 404

    data = response.json()

    return jsonify({
        "username": data["login"],
        "name": data["name"],
        "location": data["location"],
        "company": data["company"],
        "followers": data["followers"],
        "public_repos": data["public_repos"]
    })


def fetch_profile(username):
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        display_profile(data)
        calculate_exposure_score(data)
    else:
        print("Github username not found")
def display_profile(data):
    print("============================\nGITHUB PROFILE\n============================")
    print(f"Name: {data['name']}")
    print(f"Location: {data['location']}")
    print(f"Followers: {data['followers']}")
    print(f"Company: {data['company']}")
    print(f"Public repos: {data['public_repos']}")
def calculate_exposure_score(data):
    score = 0
if __name__ == "__main__":
    app.run(debug=True)
