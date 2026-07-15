import requests
username = input("Enter your username: ")
def fetch_profile(username):
    response = requests.get(f"https://api.github.com/users/{username}")
    print(response.status_code)
    if response.status_code == 200:
        data = response.json()
        print("============================\nGITHUB PROFILE\n============================")
        print(f"Name: {data["name"]}")
        print(f"Location: {data["location"]}")
        print(f"Followers: {data["followers"]}")
        print(f"Company: {data["company"]}")
        print(f"Public repos: {data["public_repos"]}")
    else:
        print("Github username not found")