import requests
import re
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

    # Fetch GitHub profile
    url = f"https://api.github.com/users/{username}"
    response = requests.get(url)

    if response.status_code != 200:
        return jsonify({"error": "GitHub username not found"}), 404

    data = response.json()

    # Fetch repositories
    repos = fetch_repositories(username)
    print("Repositories found:", len(repos))

    # Currently testing the first repository
    if repos:
        findings = []

        for repo in repos:
            repo_name = repo["name"]
            files = fetch_repo_files(username, repo_name)

            for file in files:
                if not is_scannable_file(file["name"]):
                    continue

                content = fetch_file_content(file["download_url"])
                detected = detect_secrets(content)

                for secret_type in detected:
                    findings.append({
                        "repository": repo_name,
                        "file": file["path"],
                        "type": secret_type
            })

        print("Findings:", findings)

        scannable_files = [
            file for file in files
            if file["type"] == "file"
            and is_scannable_file(file["name"])
        ]

        for file in scannable_files:
            content = fetch_file_content(file["download_url"])
            findings = detect_secrets(content)

            if findings:
                print(f"{file['name']}: {findings}")

    return jsonify({
        "username": data["login"],
        "name": data["name"],
        "location": data["location"],
        "company": data["company"],
        "followers": data["followers"],
        "public_repos": data["public_repos"],
        "findings": findings
    })


def fetch_repo_files(username, repo, path=""):
    url = f"https://api.github.com/repos/{username}/{repo}/contents/{path}"
    response = requests.get(url)
    if response.status_code != 200:
        return []

    items = response.json()
    files = []
    for item in items:
        if item["type"] == "file":
            files.append(item)
        elif item["type"] == "dir":
            files.extend(
                fetch_repo_files(username, repo, item["path"])
            )
    return files


def display_profile(data):
    print("============================\nGITHUB PROFILE\n============================")
    print(f"Name: {data['name']}")
    print(f"Location: {data['location']}")
    print(f"Followers: {data['followers']}")
    print(f"Company: {data['company']}")
    print(f"Public repos: {data['public_repos']}")


def calculate_exposure_score(data):
    score = 0


def fetch_repositories(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return []


def fetch_repo_files(username, repo):
    url = f"https://api.github.com/repos/{username}/{repo}/contents"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()

    return []


def is_scannable_file(filename):
    extensions = {
        ".py", ".js", ".ts", ".java", ".cpp", ".c",
        ".html", ".css", ".json", ".xml", ".yaml", ".yml",
        ".txt", ".md", ".env"
    }

    return any(filename.lower().endswith(ext) for ext in extensions)


def fetch_file_content(file_url):
    response = requests.get(file_url)

    if response.status_code == 200:
        return response.text

    return ""


def detect_secrets(content):
    patterns = {
        "API key": r"(?i)(api[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]",
        "Password": r"(?i)(password|passwd)\s*[:=]\s*['\"][^'\"]+['\"]",
        "Secret key": r"(?i)(secret[_-]?key)\s*[:=]\s*['\"][^'\"]+['\"]",
        "Access token": r"(?i)(access[_-]?token)\s*[:=]\s*['\"][^'\"]+['\"]"
    }

    findings = []

    for secret_type, pattern in patterns.items():
        if re.search(pattern, content):
            findings.append(secret_type)

    return findings


if __name__ == "__main__":
    app.run(debug=True)