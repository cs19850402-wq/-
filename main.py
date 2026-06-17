from flask import Flask
import requests

app = Flask(__name__)

def get_trending():
    url = "https://api.github.com/search/repositories?q=stars:>1000&sort=stars&order=desc"

    headers = {
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()

    return {"items": []}

@app.route("/")
def home():

    data = get_trending()

    result = [
        "<h2>GitHub 熱門專案 TOP 10</h2>"
    ]

    for repo in data["items"][:10]:
        result.append(
            f"""
            <b>{repo['full_name']}</b><br>
            ⭐ Stars: {repo['stargazers_count']}<br>
            🔗 <a href="{repo['html_url']}">{repo['html_url']}</a>
            <hr>
            """
        )

    return "".join(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
